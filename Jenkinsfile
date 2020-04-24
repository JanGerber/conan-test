def artifactoryServer
def artifactoryServerName
def artifactoryConanClient
def branchName =  (env.BRANCH_NAME).replaceAll("/", "_").replace("release_", "staging_")
def buildInfo


pipeline
{
    agent any
    stages
    {
        stage("Conan Init")
        {
            steps
            {
                sh label:'Conan Version', script: "conan --version"
                script
                {
                    artifactoryServer = Artifactory.server 'artifactory-jan'
                    artifactoryConanClient = Artifactory.newConanClient()
                    artifactoryServerName = artifactoryConanClient.remote.add server: artifactoryServer, repo: "test-repo"
                    artifactoryConanClient.run(command:"profile new custom")
                    artifactoryConanClient.run(command:"profile update settings.compiler.libcxx=libstdc++11 custom")
                }
            }
        }
        stage("Conan Create")
        {
            parallel
            {
                stage('Debug')
                {
                    steps
                    {
                            script
                            {
                                artifactoryConanClient.run(command:"create -pr=custom -s build_type=Debug . jan/" + branchName)
                            }
                    }
                }
                stage('Release')
                {
                    steps
                    {
                            script
                            {
                               buildInfo = artifactoryConanClient.run(command:"create -pr=custom -s build_type=Release .  jan/" + branchName)
                            }
                    }
                }
            }
        }

        stage("Conan Upload")
        {
            steps
            {
                script
                {
                    String cmd = "upload TestProj/*@jan/" + branchName + " --all -r " + artifactoryServerName + " --confirm "
                    artifactoryConanClient.run(command: cmd, buildInfo: buildInfo)
                    buildInfo.retention maxBuilds: 3, deleteBuildArtifacts: true, async: true
                    artifactoryServer.publishBuildInfo buildInfo
                }
            }
        } 
    }
}