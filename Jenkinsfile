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
                sh label:'CMake version', script: "cmake --version"
                script
                {
                    artifactoryServer = Artifactory.server 'artifactory-jan'
                    artifactoryConanClient = Artifactory.newConanClient()
                    artifactoryServerName = artifactoryConanClient.remote.add server: artifactoryServer, repo: "test-repo"
                    artifactoryConanClient.run(command:"remote add artifactory http://172.17.0.3:8081/artifactory/api/conan/conan-local")
                    artifactoryConanClient.run(command:"user -p AP3WhQebfsYvJ3z1XXtnPgwp75V -r artifactory admin")
                    artifactoryConanClient.run(command:"profile new default")
                    artifactoryConanClient.run(command:"profile update settings.os=Linux default")
                    artifactoryConanClient.run(command:"profile update settings.arch=x86_64 default")
                    artifactoryConanClient.run(command:"profile update settings.arch_build=x86_64 default")
                    artifactoryConanClient.run(command:"profile update settings.compiler=gcc default")
                    artifactoryConanClient.run(command:"profile update settings.compiler.version=6 default")
                    artifactoryConanClient.run(command:"profile update settings.compiler.libcxx=libstdc++11 default")
                }
            }
        }
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

        stage("Conan Upload")
        {
                steps
                {
                    script
                    {
                        String cmd = "upload TestProj/*@jan/" + branchName + " --all -r artifactory --confirm "
                        artifactoryConanClient.run(command: cmd, buildInfo: buildInfo)
                        buildInfo.retention maxBuilds: 3, deleteBuildArtifacts: true, async: true
                        artifactoryServer.publishBuildInfo buildInfo
                    }
                }
         }
    }
}