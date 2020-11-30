# Install dependencies

## Description

This add-on demonstrates how to install Python packages from within Blender. Elevated privileges may be required, depending on the permissions set on Blender's directory.

## Implementation

### Dependencies

The required dependencies are declared at the beginning the form a tuple of `namedtuple` and the installation state of the dependencies is stored as boolean in 
[`dependencies_installed`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L43). 
Please note that this should only contain the dependencies that will need to be installed through `pip`. Other parts of your add-on can and should be imported as usual through a simple import statement instead of a dynamic import.

### Registration

The [registration](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L236) is split into three steps:

1. Register the classes related to the add-on's preferences and a panel with installation instructions.
2. Check if the required dependencies are installed and try to import them. Only proceed to 3.) if the modules can be found and set `dependencies_installed` to true.
3. Register all other classes, e.g. panels, operators, etc.

The user will see a panel with installation instructions ([`EXAMPLE_PT_warning_panel`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L158)) 
in place of the actual operators should step 2.) fail. In case it is successful, `EXAMPLE_PT_warning_panel` won't be displayed. This is because the 
[`poll`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L165) method checks `dependencies_installed`.

![image](./imgs/install-instructions.png)

### Add-on's preferences

The add-on's preferences are implemented by [`EXAMPLE_preferences`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L223), which display the 
operator [`EXAMPLE_OT_install_dependencies`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L189). This creates a button in the details section 
of the add-on's preferences that allows the user to install the required Python packages. It calls the 
[`install_pip`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L68) function to install pip and
[`install_and_import_module()`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L89) function to install and import the dependencies. If this step is 
successful the `dependencies_installed` is set to true and the remaining panels, operators, etc. are registered as well.

![image](./imgs/user-preferences-pre-install.png)

The design that requires the user to manually press a button in the preferences, instead of automatically installing the packages, is intentional. The user should give explicit consent when files are
downloaded from the internet and Python packages are installed on their system. [The Blender Foundation takes their user's privacy and security serious](https://www.blender.org/about/license/), as an 
add-on developer you should as well.

### Preparing pip

The installation of packages requires pip. Only the Windows release of Blender includes pip, therefore it is necessary to install it through [`ensurepip.bootstrap()`](https://docs.python.org/3/library/ensurepip.html#ensurepip.bootstrap) for all other operating systems
which is done in [`install_pip`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L68). `ensurepip.bootstrap()` 
[calls pip](https://github.com/python/cpython/blob/34b0598295284e3ff6cedf5c05e159ce1fa54d60/Lib/ensurepip/__init__.py#L35). During its execution pip sets the environment variable 
[`PIP_REQ_TRACKER`](https://github.com/pypa/pip/blob/326efa5c710ecf19acc3e1315477251a4cd4bd13/src/pip/_internal/req/req_tracker.py#L54) which is used as a temporary directory. Unfortunately pip doesn't remove the environment variable and subsequent calls to pip 
will attempt to use the path in `PIP_REQ_TRACKER` as temporary directory. However, this directory doesn't exist anymore and the pip would throw an exception. Therefore, `os.environ.pop("PIP_REQ_TRACKER", None)` is needed.

### Installing the package

Blender excludes the user site-packages from its `sys.path` by default and is therefore not able to import these packages. [This is done to prevent the accidental loading of packages installed by the system's Python which may be incompatible to Blender's Python version.](https://developer.blender.org/rB79a58eef059ffc3f12d11bd68938cfb1b4cd2462)
However, by default pip would still check the user site-packages when it tries to determine if the requirements are already satisfied. That would be incorrect for Blender, since it needs them to be installed for its own Python interpreter.
Therefore, [`PYTHONNOUSERSITE`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONNOUSERSITE) is temporarily set to prevent pip from checking the user site-packages when trying to determine if the packages are already 
installed. The package installation is accomplished by [calling pip through `subprocess`](https://github.com/robertguetzkow/blender-python-examples/blob/4a3c99a843305b91e05db386559905b23cf6eb87/add-ons/install-dependencies/install-dependencies.py#L117). The path to the 
Python binary is given by [`sys.executable`](https://developer.blender.org/rB04c5471ceefb41c9e49bf7c86f07e9e7b8426bb3). If you need to support Blender versions prior to 2.91.0, then you have to check [`bpy.app.version`](https://docs.blender.org/api/current/bpy.app.html#bpy.app.version) 
and use `bpy.app.binary_path_python` in older versions of Blender. Once the installation has been attempted, the `PYTHONNOUSERSITE` environment variable is removed.

### Importing the module

The programmatic import is done through [`importlib.import_module()`](https://docs.python.org/3/library/importlib.html#importlib.import_module) and the result is assigned to the global symbol table dictionary 
returned by [`globals()`](https://docs.python.org/3/library/functions.html#globals).

## The user's perspective

The user installs the add-on through the user preferences (*Edit > Preferences > Add-ons*). They might check the sidebar where they expect to find the add-on's operators, but find the panel with the installation instructions instead.
Hence they go back to the preferences, open the details section of the add-on and press the button to install the dependencies. Once the install is completed the tab in the sidebar shows all operators as expected.

Failures during installation are reported to the user in a popup. In case the add-on is executed as a script, instead of being installed as add-on, it will display the installation instructions in the sidebar as well.

## Improvement suggestions for your own add-on

- Show a more descriptive error message when a "permission denied" error occurs during the installation of packages. Inform the user that elevated permission are necessary and provide instructions to resolve the issue. Ideally Blender shouldn't be started with
 elevated permissions, since this would be against security best practice. Therefore, you could provide instructions to install the packages manually and include a `requirements.txt`.

## Additional Information

The add-on was originally developed as an answer to the [this question](https://blender.stackexchange.com/questions/168448/bundling-python-library-with-addon) on Blender's StackExchange.

## Change log

### 1.0.4 - 2020-11-30
 **Compatible Blender versions:** 2.91

 **Commit hash:** [8bf7ddefb458e697d51ca5bd74185890146d4e9d](https://github.com/robertguetzkow/blender-python-examples/commit/8bf7ddefb458e697d51ca5bd74185890146d4e9d)

 **Changes:**
 - Replace the [deprecated `bpy.app.binary_path_python`](https://developer.blender.org/rB04c5471ceefb41c9e49bf7c86f07e9e7b8426bb3) with `sys.executable`. For compatibility with version prior to 2.91.0 you would have to modify the code. Check [`bpy.app.version`](https://docs.blender.org/api/current/bpy.app.html#bpy.app.version) and select the appropriate way to get the path to the Python interpreter for that Blender version.
 - Simplify handling of environment variables (see #3).
 - Check if the dependecy has a `__version__` attribute, before attempting to display it in a label. This fix was suggested by @StefanKarlsson987.

### 1.0.3 - 2020-10-19

 **Compatible Blender versions:** 2.81 to 2.90

 **Commit hash:** [8bf7ddefb458e697d51ca5bd74185890146d4e9d](https://github.com/robertguetzkow/blender-python-examples/commit/8bf7ddefb458e697d51ca5bd74185890146d4e9d)

 **Changes:**
 - Prevent pip from checking the user site-packages to determine if requirements are satisfied. Blender cannot import packages from user site-packages by default, as this has been intentionally disabled by commit [rB79a58eef059ffc3f12d11bd68938cfb1b4cd2462](https://developer.blender.org/rB79a58eef059ffc3f12d11bd68938cfb1b4cd2462).

### 1.0.2 - 2020-05-20

 **Compatible Blender versions:** 2.81 to 2.90

 **Commit hash:** [cd3597939d77e37bb45434533440d56262f01a55](https://github.com/robertguetzkow/blender-python-examples/commit/cd3597939d77e37bb45434533440d56262f01a55)

 **Changes:**
 - Fix `install_pip` for when the ensurepip module is not available but pip is already installed

### 1.0.1 - 2020-05-19

 **Compatible Blender versions:** 2.81 to 2.90

 **Commit hash:** [211e51a3ac2a83f4f1db5a80c59eded138acbf40](https://github.com/robertguetzkow/blender-python-examples/commit/211e51a3ac2a83f4f1db5a80c59eded138acbf40)

 **Changes:**
 - Refactor `install_and_import_module()` and place installation of pip in a separate function `install_pip`

### 1.0.0 - 2020-05-18

 **Compatible Blender versions:** 2.81 to 2.90

 **Commit hash:** [226ef43cf003511b6220e7135d4b6a8289729582](https://github.com/robertguetzkow/blender-python-examples/commit/226ef43cf003511b6220e7135d4b6a8289729582)

 **Changes:**
 - Initial version
