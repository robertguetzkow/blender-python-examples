# Install dependencies

## Description

This add-on demonstrates how to install Python packages from within Blender. Elevated privileges may be required, depending on the permissions set on Blender's directory.

## Implementation

### Dependencies

The required dependencies are declared at the beginning the form a tuple of `namedtuple` and the installation state of the dependencies is stored as boolean in [`dependencies_installed`](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L41).

### Registration

The [registration](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L211) is split into three steps:

1. Register the classes related to the add-on's preferences and a panel with installation instructions.
2. Check if the required dependencies are installed and try to import them. Only proceed to 3.) if the modules can be found and set `dependencies_installed` to true.
3. Register all other classes, e.g. panels, operators, etc.

The user will see a panel with installation instructions ([`EXAMPLE_PT_warning_panel`](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L134)) 
in place of the actual operators should step 2.) fail. In case it is successful, `EXAMPLE_PT_warning_panel` won't be displayed. This is because the [`poll`](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L141) 
method checks `dependencies_installed`.

![image](./imgs/install-instructions.png)

### Add-on's preferences

The add-on's preferences are implemented by [`EXAMPLE_preferences`](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L198), which display the 
operator [`EXAMPLE_OT_install_dependencies`](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L165). This creates a button in the details section 
of the add-on's preferences that allows the user to install the required Python packages. It calls the [`install_and_import_module()`](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L63)
function to install and import the dependencies. If this step is successful the `dependencies_installed` is set to true and the remaining panels, operators, etc. are registered as well.

![image](./imgs/user-preferences-pre-install.png)

The design that requires the user to manually press a button in the preferences, instead of automatically installing the packages, is intentional. The user should give explicit consent when files are
downloaded from the internet and Python packages are installed on their system. [The Blender Foundation takes their users privacy and security serious](https://www.blender.org/about/license/), as an 
add-on developer you should as well.

### Preparing pip

The installation of packages with [`install_and_import_module()`](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L63) requires pip. Only the Windows 
release of Blender 2.81 includes pip, therefore it is necessary to install it through [`ensurepip.bootstrap()`](https://docs.python.org/3/library/ensurepip.html#ensurepip.bootstrap). `ensurepip.bootstrap()` 
[calls pip](https://github.com/python/cpython/blob/34b0598295284e3ff6cedf5c05e159ce1fa54d60/Lib/ensurepip/__init__.py#L35). During its execution pip sets the environment variable 
[`PIP_REQ_TRACKER`](https://github.com/pypa/pip/blob/326efa5c710ecf19acc3e1315477251a4cd4bd13/src/pip/_internal/req/req_tracker.py#L54) which is used as a temporary directory. Unfortunately pip doesn't remove the environment variable and subsequent calls to pip 
will attempt to use the path in `PIP_REQ_TRACKER` as temporary directory. However, this directory doesn't exist anymore and the pip would throw an exception. Therefore, `os.environ.pop("PIP_REQ_TRACKER", None)` is needed.

### Installing the package

The package installation is accomplished by [calling pip through `subprocess`](https://github.com/robertguetzkow/blender-python-examples/blob/226ef43cf003511b6220e7135d4b6a8289729582/add-ons/install-dependencies/install-dependencies.py#L95). The path to the 
Python binary is given by [`bpy.app.binary_path_python`](https://docs.blender.org/api/current/bpy.app.html#bpy.app.binary_path_python).

### Importing the module

The programmatic import is done through [`importlib.import_module()`](https://docs.python.org/3/library/importlib.html#importlib.import_module) and the result is assigned to the global symbol table dictionary 
returned by [`globals()`](https://docs.python.org/3/library/functions.html#globals).

## The user's perspective

The user installs the add-on through the user preferences (*Edit > Preferences > Add-ons*). They might check the sidebar where they expect to find the add-on's operators, but find the panel with the installation instructions instead.
Hence they go back to the preferences, open the details section of the add-on and press the button to install the dependencies. Once the install is completed the tab in the sidebar shows all operators as expected

## Additional Information

The add-on was originally developed as an answer to the [this question](https://blender.stackexchange.com/questions/168448/bundling-python-library-with-addon) on Blender's StackExchange.


## Change log
### [1.0.0]() - 2020-05-18

 **Compatible Blender versions:** 2.81 to 2.90

 **Commit hash:** 226ef43cf003511b6220e7135d4b6a8289729582

 **Changes:**
 - Initial commit
