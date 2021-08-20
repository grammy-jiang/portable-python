from portable_python.builder import BuildSetup, ModuleBuilder


@BuildSetup.module_builders.declare
class LibFFI(ModuleBuilder):

    # telltale = ["/usr/share/doc/libffi-dev", "{include}/ffi/ffi.h"]
    telltale = "/usr/share/doc/libffi-dev"

    @property
    def url(self):
        return f"https://github.com/libffi/libffi/releases/download/v{self.version}/libffi-{self.version}.tar.gz"

    @property
    def version(self):
        return "3.3"

    def xenv_cflags(self):
        yield "-fPIC"
        if self.target.is_macos:
            yield "-isysroot", self.target.sdk_folder

    def _do_linux_compile(self):
        self.run_configure()
        self.run("make")
        self.run("make", "install", "DESTDIR=%s" % self.deps.parent)


@BuildSetup.module_builders.declare
class Readline(ModuleBuilder):
    """
    TODO: readline is not getting picked up
    macos: fails with Symbol not found: _rl_catch_signals (or earlier: _free_history_entry)
    linux: builds OK, but version is incorrect (system readline, instead of the one we compiled)
    """

    telltale = "{include}/readline/readline.h"

    @property
    def url(self):
        return f"https://ftp.gnu.org/gnu/readline/readline-{self.version}.tar.gz"

    @property
    def version(self):
        return "8.1"

    def c_configure_args(self):
        yield from super().c_configure_args()
        yield "--disable-install-examples"
        yield "--with-curses"

    def _do_linux_compile(self):
        self.run_configure()
        args = []
        if self.target.is_linux:
            # See https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/readline.rb
            args.append("SHLIB_LIBS=-lcurses")
            # self.setup.patch_file(self.build_folder / "readline.pc", "Requires.private:", "# Requires.private:")

        self.run("make", *args)
        self.run("make", "install", "DESTDIR=%s" % self.deps.parent)


@BuildSetup.module_builders.declare
class Openssl(ModuleBuilder):

    c_configure_program = "./Configure"
    telltale = "{include}/openssl/ssl.h"

    @property
    def url(self):
        return f"https://www.openssl.org/source/openssl-{self.version}.tar.gz"

    @property
    def version(self):
        return "1.1.1k"

    def c_configure_args(self):
        yield from super().c_configure_args()
        yield "--openssldir=/deps"
        yield "-DPEDANTIC"
        if self.target.is_macos:
            yield "darwin64-%s-cc" % self.target.architecture

        else:
            yield "%s-%s" % (self.target.platform, self.target.architecture)

        yield "no-shared"

    def _do_linux_compile(self):
        self.run_configure()
        self.run("make")
        self.run("make", "install", "DESTDIR=%s" % self.deps.parent)


@BuildSetup.module_builders.declare
class Uuid(ModuleBuilder):

    needs_platforms = ["linux"]
    telltale = "{include}/uuid/uuid.h"

    @property
    def url(self):
        return f"https://sourceforge.net/projects/libuuid/files/libuuid-{self.version}.tar.gz"

    @property
    def version(self):
        return "1.0.3"

    def _do_linux_compile(self):
        self.run_configure()
        self.run("make")
        self.run("make", "install", "DESTDIR=%s" % self.deps.parent)
