from conans import ConanFile, CMake


class HelloConan(ConanFile):
    name = "TestProj"
    version = "1.0"
    license = " "
    description = "This is a test project for conan"
    url = "https://github.com/JanGerber/conan-test"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "src/*"
    revision_mode = "scm"


    def build(self):
        for bt in ("Debug", "Release"):
            cmake = CMake(self, build_type=bt)
            cmake.configure(source_folder="src")
            cmake.build()
            cmake.install()
