name: Comprehensive Test
on:
  workflow_dispatch:
    inputs: 
      gitcode_owner:
        description: 'GitCode 用户名，项目 URL 中可获取'
        required: true
        default: NiceLeee
      gitcode_repo:
        description: 'GitCode 项目名，项目 URL 中可获取'
        required: true
        default: NiceLeee
      gitcode_token:
        description: 'GitCode api token'
        required: true
jobs:
  # Job 1: 测试单文件创建 release 和相关操作
  test-single-file:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        ref: ${{ github.event.ref }}
        
    - name: Test create release with single file
      id: create_release_single
      uses: ./
      with:
        gitcode_action: create_release
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-single-${{ github.run_number }}
        gitcode_release_name: Single File Test v1.0-${{ github.run_number }}
        gitcode_release_body: 'GitCode single file release test'
        gitcode_target_commitish: master
        gitcode_file_name: 'single-test.txt'
        gitcode_file_path: 'LICENSE'
          
    - name: Test upload additional single file to existing release
      uses: ./
      with:
        gitcode_action: upload_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_release_id: ${{ steps.create_release_single.outputs.release-id }}
        gitcode_file_name: 'additional-single.txt'
        gitcode_file_path: 'README.md'

    - name: Test upload using tag_name (single)
      uses: ./
      with:
        gitcode_action: upload_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-single-${{ github.run_number }}
        gitcode_file_name: 'tag-upload-single.txt'
        gitcode_file_path: 'action.yml'
        
    - name: Test update asset
      uses: ./
      with:
        gitcode_action: update_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-single-${{ github.run_number }}
        gitcode_old_asset_name: 'single-test.txt'
        gitcode_new_file_path: 'requirements.txt'
        
    - name: Test delete specific asset
      uses: ./
      with:
        gitcode_action: delete_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-single-${{ github.run_number }}
        gitcode_delete_assets: 'tag-upload-single.txt'
        
    - name: Test delete release
      uses: ./
      with:
        gitcode_action: delete_release
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-single-${{ github.run_number }}

  # Job 2: 测试多文件创建 release 和相关操作
  test-multi-file:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        ref: ${{ github.event.ref }}
        
    - name: Test create release with multiple files
      id: create_release_multi
      uses: ./
      with:
        gitcode_action: create_release
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-multi-${{ github.run_number }}
        gitcode_release_name: Multi File Test v1.0-${{ github.run_number }}
        gitcode_release_body: 'GitCode multi file release test'
        gitcode_target_commitish: master
        gitcode_files: |
          LICENSE
          README.md
          action.yml
          
    - name: Test upload additional multiple files to existing release
      uses: ./
      with:
        gitcode_action: upload_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_release_id: ${{ steps.create_release_multi.outputs.release-id }}
        gitcode_files: |
          requirements.txt
          gitcode_release.py

    - name: Test upload using tag_name (multi)
      uses: ./
      with:
        gitcode_action: upload_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-multi-${{ github.run_number }}
        gitcode_file_name: 'tag-upload-multi.txt'
        gitcode_file_path: 'LICENSE'
        
    - name: Test delete multiple assets
      uses: ./
      with:
        gitcode_action: delete_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-multi-${{ github.run_number }}
        gitcode_delete_assets: |
          tag-upload-multi.txt
          LICENSE
        
    - name: Test delete release
      uses: ./
      with:
        gitcode_action: delete_release
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-multi-${{ github.run_number }}

  # Job 3: 测试使用已存在 release ID 的场景
  test-existing-release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        ref: ${{ github.event.ref }}
        
    - name: Create base release for testing
      id: create_base_release
      uses: ./
      with:
        gitcode_action: create_release
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-existing-${{ github.run_number }}
        gitcode_release_name: Existing Release Test v1.0-${{ github.run_number }}
        gitcode_release_body: 'Test using existing release ID'
        gitcode_target_commitish: master
        
    - name: Test upload single file to existing release by ID
      uses: ./
      with:
        gitcode_action: upload_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_release_id: ${{ steps.create_base_release.outputs.release-id }}
        gitcode_file_name: 'existing-single.txt'
        gitcode_file_path: 'LICENSE'
        
    - name: Test upload multiple files to existing release by ID
      uses: ./
      with:
        gitcode_action: upload_asset
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_release_id: ${{ steps.create_base_release.outputs.release-id }}
        gitcode_files: |
          README.md
          action.yml
          requirements.txt
        
    - name: Test delete release
      uses: ./
      with:
        gitcode_action: delete_release
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: v1.0-existing-${{ github.run_number }}
                
def upload_assets(gitcode_files, gitcode_client, gitcode_repo, gitcode_release_id):
    result = []
    uploaded_path = set()
    for file_path_pattern in gitcode_files:
        file_path_pattern = file_path_pattern.strip()
        recursive = True if "**" in file_path_pattern else False
        files = glob.glob(file_path_pattern, recursive = recursive)
        if len(files) == 0:
            raise ValueError('file_path_pattern does not match: ' + file_path_pattern)
        for file_path in files:
            if file_path in uploaded_path or os.path.isdir(file_path):
                continue
            success, msg = gitcode_client.upload_asset(gitcode_repo, gitcode_release_id, file_name = os.path.basename(file_path), file_path = file_path)
            if not success:
                raise Exception("Upload file asset failed: " + msg)
            result.append(msg)
            uploaded_path.add(file_path)
    return result
    
def create_release():
    gitcode_owner = get('gitcode_owner')
    gitcode_token = get('gitcode_token')
    gitcode_repo = get('gitcode_repo')
    gitcode_tag_name = get('gitcode_tag_name')
    gitcode_release_name = get('gitcode_release_name')
    gitcode_release_body = get('gitcode_release_body')
    gitcode_target_commitish = get('gitcode_target_commitish')
    
    gitcode_files = os.environ.get('gitcode_files')
    if gitcode_files:
        gitcode_files = gitcode_files.strip().split("\n")
    else:
        gitcode_file_name = os.environ.get('gitcode_file_name')
        gitcode_file_path = os.environ.get('gitcode_file_path')
        if (gitcode_file_name and not gitcode_file_path) or (gitcode_file_path and not gitcode_file_name):
            raise ValueError('gitcode_file_name and gitcode_file_path should be set together')
        if gitcode_file_path and not os.path.isfile(gitcode_file_path):
            raise ValueError('gitcode_file_path not exists: ' + gitcode_file_path)
    
    gitcode_client = GitCode(owner = gitcode_owner, token = gitcode_token)
    success, release_id = gitcode_client.create_release(repo = gitcode_repo, tag_name = gitcode_tag_name, name = gitcode_release_name, 
                body = gitcode_release_body, target_commitish = gitcode_target_commitish)
    if success:
        print(f"Release created successfully with ID: {release_id}")
        set_result("release-id", release_id)
        
        # Upload files if provided
        if gitcode_files:
            result = upload_assets(gitcode_files, gitcode_client, gitcode_repo, release_id)
            if result:
                set_result("download-url", '\n'.join(result))
        elif gitcode_file_path:
            success, msg = gitcode_client.upload_asset(gitcode_repo, release_id, file_name = gitcode_file_name, file_path = gitcode_file_path)
            if not success:
                raise Exception("Upload file asset failed: " + msg)
            set_result("download-url", msg)
    else:
        raise Exception("Create release failed: " + str(release_id))

def upload_asset():
    gitcode_owner = get('gitcode_owner')
    gitcode_repo = get('gitcode_repo')
    gitcode_token = get('gitcode_token')
    gitcode_files = os.environ.get('gitcode_files')
    
    gitcode_client = GitCode(owner = gitcode_owner, token = gitcode_token)

    gitcode_release_id = os.environ.get('gitcode_release_id')
    if not gitcode_release_id:
        gitcode_tag_name = get('gitcode_tag_name')
        success, gitcode_release_id = gitcode_client.get_release_by_tag(gitcode_repo, gitcode_tag_name)
        if not success:
            raise Exception(f"Failed to get release by tag {gitcode_tag_name}")

    if gitcode_files:
        gitcode_files = gitcode_files.strip().split("\n")
        result = upload_assets(gitcode_files, gitcode_client, gitcode_repo, gitcode_release_id)
        set_result("download-url", '\n'.join(result))
    else:
        gitcode_file_name = get('gitcode_file_name')
        gitcode_file_path = get('gitcode_file_path')
        if gitcode_file_path and not os.path.isfile(gitcode_file_path):
            raise ValueError('gitcode_file_path not exists: ' + gitcode_file_path)
        success, msg = gitcode_client.upload_asset(gitcode_repo, gitcode_release_id, file_name = gitcode_file_name, file_path = gitcode_file_path)
        if not success:
            raise Exception("Upload file asset failed: " + msg)
        set_result("download-url", msg)

def delete_release():
    gitcode_owner = get('gitcode_owner')
    gitcode_repo = get('gitcode_repo')
    gitcode_token = get('gitcode_token')
    gitcode_tag_name = get('gitcode_tag_name')
    
    gitcode_client = GitCode(owner=gitcode_owner, token=gitcode_token)
    success, msg = gitcode_client.delete_release_by_tag(gitcode_repo, gitcode_tag_name)
    if not success:
        raise Exception("Delete release failed: " + msg)
    print("Release deleted successfully")

def delete_asset():
    gitcode_owner = get('gitcode_owner')
    gitcode_repo = get('gitcode_repo')
    gitcode_token = get('gitcode_token')
    gitcode_tag_name = get('gitcode_tag_name')
    
    gitcode_delete_assets = get('gitcode_delete_assets')
    asset_names = [name.strip() for name in gitcode_delete_assets.strip().split('\n') if name.strip()]
    
    gitcode_client = GitCode(owner=gitcode_owner, token=gitcode_token)
    
    for asset_name in asset_names:
        success, msg = gitcode_client.delete_asset_by_filename(gitcode_repo, gitcode_tag_name, asset_name)
        if not success:
            raise Exception(f"Delete asset {asset_name} failed: " + msg)
        print(f"Asset {asset_name} deleted successfully")

def update_asset():
    gitcode_owner = get('gitcode_owner')
    gitcode_repo = get('gitcode_repo')
    gitcode_token = get('gitcode_token')
    gitcode_tag_name = get('gitcode_tag_name')
    gitcode_old_asset_name = get('gitcode_old_asset_name')
    gitcode_new_file_path = get('gitcode_new_file_path')
    
    if not os.path.isfile(gitcode_new_file_path):
        raise ValueError('gitcode_new_file_path not exists: ' + gitcode_new_file_path)
    
    gitcode_client = GitCode(owner=gitcode_owner, token=gitcode_token)
    success, msg = gitcode_client.update_asset(gitcode_repo, gitcode_tag_name, gitcode_old_asset_name, gitcode_new_file_path)
    if not success:
        raise Exception("Update asset failed: " + msg)
    print(f"Asset {gitcode_old_asset_name} updated successfully")
    set_result("download-url", msg)
        
if __name__ == "__main__":
    gitcode_action = os.environ.get("gitcode_action")
    
    if gitcode_action == "create_release":
        create_release()
    elif gitcode_action == "upload_asset":
        upload_asset()
    elif gitcode_action == "delete_release":
        delete_release()
    elif gitcode_action == "delete_asset":
        delete_asset()
    elif gitcode_action == "update_asset":
        update_asset()
    else:
        raise ValueError(f"Unknown action: {gitcode_action}. Supported actions: create_release, upload_asset, delete_release, delete_asset, update_asset")
