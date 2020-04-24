def artifactoryServer
def artifactoryServerName
def artifactoryConanClient
def branchName =  (env.BRANCH_NAME).replaceAll("/", "_").replace("release_", "staging_")
def buildInfo


pipeline
{
    agent
    {
        node
        {
            label "test-node"
        }
    }
    stages
    {
        stage("Conan Init")
        {
            steps
            {
                bat label:'Conan Version', script: "conan --version"
                script
                {
                    artifactoryServer = Artifactory.server 'jan artifactory'
                    artifactoryConanClient = Artifactory.newConanClient()
                    artifactoryServerName = artifactoryConanClient.remote.add server: artifactoryServer, repo: "test-repo"
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
                                artifactoryConanClient.run(command:"create -s build_type=Debug . jan/" + branchName)
                            }
                    }
                }
                stage('Release')
                {
                    steps
                    {
                            script
                            {
                               buildInfo = artifactoryConanClient.run(command:"create -s build_type=Release .  jan/" + branchName)
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