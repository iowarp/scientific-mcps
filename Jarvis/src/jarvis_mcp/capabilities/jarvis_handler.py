from fastapi import HTTPException
from jarvis_cd.basic.pkg import Pipeline
from jarvis_cd.basic.jarvis_manager import JarvisManager
import os

async def create_pipeline(pipeline_id: str) -> dict:
    try:
        Pipeline().create(pipeline_id).build_env().save()
        return {"pipeline_id": pipeline_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Create failed: {e}")

async def load_pipeline(pipeline_id: str = None) -> dict:
    try:
        pipeline = Pipeline().load(pipeline_id)
        return {"pipeline_id": pipeline_id, "status": "loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Load failed: {e}")

async def append_pkg(
    pipeline_id: str,
    pkg_type: str,
    pkg_id: str = None,
    do_configure: bool = True,
    **kwargs
) -> dict:
    try:
        # Avoid duplicate do_configure in kwargs
        raw_kwargs = dict(kwargs)
        config_flag = do_configure
        if 'do_configure' in raw_kwargs:
            config_flag = raw_kwargs.pop('do_configure')

        pipeline = Pipeline().load(pipeline_id)
        pipeline.append(
            pkg_type,
            pkg_id=pkg_id,
            do_configure=config_flag,
            **raw_kwargs
        ).save()
        return {"pipeline_id": pipeline_id, "appended": pkg_type}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Append failed: {e}")


async def build_pipeline_env(pipeline_id: str) -> dict:
    """
    Load a Jarvis-CD pipeline, rebuild its environment cache,
    tracking only CMAKE_PREFIX_PATH and PATH from the current shell, then save.
    """
    try:
        # 1. Load the existing pipeline
        pipeline = Pipeline().load(pipeline_id)

        # 2. Always track these two vars
        default_keys = ["CMAKE_PREFIX_PATH", "PATH"]
        env_track_dict = {key: True for key in default_keys}

        # 3. Rebuild the env cache, track only those vars, and save
        pipeline.build_env(env_track_dict).save()

        return {
            "pipeline_id": pipeline_id,
            "status": "environment_built"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Build env failed: {e}")


async def update_pipeline(pipeline_id: str) -> dict:
    """
    Re-apply the current environment & configuration to every pkg in the pipeline,
    then persist the updated pipeline.
    """
    try:
        pipeline = Pipeline().load(pipeline_id)
        pipeline.update()  # re-run configure on all sub-pkgs
        pipeline.save()    # persist any changes
        return {"pipeline_id": pipeline_id, "status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {e}")


async def configure_pkg(pipeline_id: str, pkg_id: str, **kwargs) -> dict:
    try:
        pipeline = Pipeline().load(pipeline_id)
        # configure the pkg (this does NOT return self)
        pipeline.configure(pkg_id, **kwargs)

        # now save the entire pipeline (which will recurse and save each sub-pkg)
        pipeline.save()
        return {"pipeline_id": pipeline_id, "configured": pkg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configure failed: {e}")

async def get_pkg_config(pipeline_id: str, pkg_id: str) -> dict:
    try:
        # 1. Load the pipeline
        pipeline = Pipeline().load(pipeline_id)

        # 2. Lookup the pkg
        pkg = pipeline.get_pkg(pkg_id)
        if pkg is None:
            raise HTTPException(status_code=404, detail=f"Package '{pkg_id}' not found")

        # 3. Return its config dict
        return {
            "pipeline_id": pipeline.global_id,
            "pkg_id": pkg_id,
            "config": pkg.config
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get config failed: {e}")

async def unlink_pkg(pipeline_id: str, pkg_id: str) -> dict:
    try:
        Pipeline().load(pipeline_id).unlink(pkg_id).save()
        return {"pipeline_id": pipeline_id, "unlinked": pkg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unlink failed: {e}")

async def remove_pkg(pipeline_id: str, pkg_id: str) -> dict:
    try:
        Pipeline().load(pipeline_id).remove(pkg_id).save()
        return {"pipeline_id": pipeline_id, "removed": pkg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Remove failed: {e}")

async def run_pipeline(pipeline_id: str) -> dict:
    try:
        Pipeline().load(pipeline_id).run()
        return {"pipeline_id": pipeline_id, "status": "running"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Run failed: {e}")

async def destroy_pipeline(pipeline_id: str) -> dict:
    try:
        Pipeline().load(pipeline_id).destroy()
        return {"pipeline_id": pipeline_id, "status": "destroyed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Destroy failed: {e}")

async def get_all_packages() -> dict:
    """
    Get a comprehensive list of all available packages across all repositories.
    Returns package names, types, descriptions, capabilities, and configuration options.
    """
    try:
        manager = JarvisManager.get_instance()
        all_packages = {}
        
        # Get all repositories
        for repo in manager.repos:
            repo_name = repo['name']
            repo_path = repo['path']
            
            if not os.path.exists(repo_path):
                continue
                
            # Look for packages in the repository
            packages_dir = os.path.join(repo_path, repo_name)
            if os.path.exists(packages_dir):
                for item in os.listdir(packages_dir):
                    pkg_path = os.path.join(packages_dir, item)
                    if os.path.isdir(pkg_path) and not item.startswith('_'):
                        # Try to get package information
                        pkg_file = os.path.join(pkg_path, 'pkg.py')
                        readme_file = os.path.join(pkg_path, 'README.md')
                        
                        description = "No description available"
                        capabilities = []
                        config_options = {}
                        
                        # Extract description from README first
                        if os.path.exists(readme_file):
                            try:
                                with open(readme_file, 'r') as f:
                                    lines = f.readlines()[:5]  # First 5 lines
                                    description = ' '.join([line.strip() for line in lines if line.strip()])[:300]
                            except:
                                pass
                        
                        # Extract capabilities and config from pkg.py
                        if os.path.exists(pkg_file):
                            try:
                                with open(pkg_file, 'r') as f:
                                    content = f.read()
                                    
                                    # Extract class docstring
                                    if description == "No description available":
                                        import re
                                        docstring_match = re.search(r'class.*?"""(.*?)"""', content, re.DOTALL)
                                        if docstring_match:
                                            description = docstring_match.group(1).strip()[:300]
                                    
                                    # Extract configuration menu items to understand capabilities
                                    if '_configure_menu' in content:
                                        # Try to extract menu configuration dynamically
                                        try:
                                            # Construct a temporary package to get config menu
                                            pkg_obj = manager.construct_pkg(item)
                                            if hasattr(pkg_obj, '_configure_menu'):
                                                menu_items = pkg_obj._configure_menu()
                                                for config in menu_items:
                                                    param_name = config.get('name', 'unknown')
                                                    param_type = config.get('type', 'str').__name__ if hasattr(config.get('type'), '__name__') else str(config.get('type', 'unknown'))
                                                    param_default = config.get('default', None)
                                                    param_choices = config.get('choices', [])
                                                    param_msg = config.get('msg', '')
                                                    
                                                    config_options[param_name] = {
                                                        'type': param_type,
                                                        'default': param_default,
                                                        'description': param_msg,
                                                        'choices': param_choices
                                                    }
                                        except Exception as e:
                                            # If we can't construct the package, skip capability extraction
                                            pass
                                    
                                    # Look for common capability patterns in the code
                                    capability_patterns = {
                                        'configurable_block_sizes': ['block_size', 'xfer', 'buffer_size'],
                                        'parallel_execution': ['nprocs', 'ppn', 'mpi'],
                                        'read_operations': ['read', 'input'],
                                        'write_operations': ['write', 'output'],
                                        'supports_hdf5': ['hdf5', 'h5'],
                                        'supports_mpiio': ['mpiio', 'mpi-io'],
                                        'supports_posix': ['posix'],
                                        'api_selection': ['api']
                                    }
                                    
                                    for capability, patterns in capability_patterns.items():
                                        if any(pattern in content.lower() for pattern in patterns):
                                            capabilities.append(capability)
                                            
                            except Exception as e:
                                # If we can't read the file, continue with empty capabilities
                                pass
                        
                        all_packages[item] = {
                            "name": item,
                            "repository": repo_name,
                            "description": description,
                            "path": pkg_path,
                            "available": os.path.exists(pkg_file),
                            "capabilities": capabilities,
                            "configuration_options": config_options,
                            "total_config_params": len(config_options)
                        }
        
        return {
            "status": "success",
            "total_packages": len(all_packages),
            "repositories_scanned": len(manager.repos),
            "packages": all_packages
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get packages failed: {e}")
