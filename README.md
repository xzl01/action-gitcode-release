name: 'action-gitcode-release'
description: '在 GitCode 项目发布 release(可以上传附件)'
inputs:
  gitcode_action:
    description: '执行的操作类型：create_release, upload_asset, delete_release, delete_asset, update_asset'
    required: true

  gitcode_owner:
    description: 'GitCode 用户名，项目 URL 中可获取'
    required: true
  gitcode_repo:
    description: 'GitCode 项目名，项目 URL 中可获取'
    required: true
  gitcode_token:
    description: 'GitCode api token'
    required: true
    
  gitcode_tag_name:
    description: 'GitCode Tag 名称，提倡以 v 字母为前缀做为 Release 名称，例如 v1.0 或者 v2.3.4'
    required: false
  gitcode_release_name:
    description: 'GitCode release 名称'
    required: false
  gitcode_release_body:
    description: 'GitCode release 描述'
    required: false
  gitcode_target_commitish:
    description: 'GitCode 分支名称或者 commit SHA'
    required: false

  gitcode_files:
    description: '上传的附件列表 (多个文件)'
    required: false
    
  gitcode_file_name:
    description: '上传的附件名称 (单个文件)'
    required: false
  gitcode_file_path:
    description: '上传的附件的本地路径 (单个文件)'
    required: false
    
  gitcode_release_id:
    description: '指定的 release ID (upload_asset 操作时可选，优先级高于 tag_name)'
    required: false
    
  gitcode_upload_retry_times:
    description: '上传附件失败后的尝试次数'
    required: false

  gitcode_delete_asset:
    description: '要删除的单个附件名称 (delete_asset 操作时使用)'
    required: false
  gitcode_delete_assets:
    description: '要删除的多个附件名称，每行一个文件名 (delete_asset 操作时使用)'
    required: false
    
  gitcode_old_asset_name:
    description: '要更新的旧附件名称 (update_asset 操作时使用)'
    required: false
  gitcode_new_file_path:
    description: '新附件的本地路径 (update_asset 操作时使用)'
    required: false
    
outputs:
  release-id:
    description: '创建的 release 的 id'
    value: ${{ steps.release.outputs.release-id }}
  download-url:
    description: '附件的下载地址'
    value: ${{ steps.release.outputs.download-url }}
runs:
  using: "composite"
  steps:
    - name: Execute GitCode Release Action
      id: release
      shell: bash
      env:
        gitcode_action: ${{ inputs.gitcode_action }}
        gitcode_owner: ${{ inputs.gitcode_owner }}
        gitcode_repo: ${{ inputs.gitcode_repo }}
        gitcode_token: ${{ inputs.gitcode_token }}
        gitcode_tag_name: ${{ inputs.gitcode_tag_name }}
        gitcode_release_name: ${{ inputs.gitcode_release_name }}
        gitcode_release_body: ${{ inputs.gitcode_release_body }}
        gitcode_target_commitish: ${{ inputs.gitcode_target_commitish }}
        gitcode_files: ${{ inputs.gitcode_files }}
        gitcode_file_name: ${{ inputs.gitcode_file_name }}
        gitcode_file_path: ${{ inputs.gitcode_file_path }}
        gitcode_release_id: ${{ inputs.gitcode_release_id }}
        gitcode_upload_retry_times: ${{ inputs.gitcode_upload_retry_times }}
        gitcode_delete_asset: ${{ inputs.gitcode_delete_asset }}
        gitcode_delete_assets: ${{ inputs.gitcode_delete_assets }}
        gitcode_old_asset_name: ${{ inputs.gitcode_old_asset_name }}
        gitcode_new_file_path: ${{ inputs.gitcode_new_file_path }}
      run: |
        pip install -r "${{ github.action_path }}/requirements.txt"
        python "${{ github.action_path }}/gitcode_release.py"

# Ref: https://haya14busa.github.io/github-action-brandings/
branding:
  icon: "square"
  color: "blue"```

### 4.3. 向已有 release 上传单个附件（通过 release_id 定位）

```yaml
- name: Upload Single Asset to Existing Release by ID
  uses: nicennnnnnnlee/action-gitcode-release@master
  with:
    gitcode_action: upload_asset
    gitcode_owner: GitCode 用户名
    gitcode_repo: GitCode 项目名
    gitcode_token: ${{ secrets.gitcode_token }}
    gitcode_release_id: 12345
    gitcode_upload_retry_times: 3
    gitcode_file_name: 新附件名称
    gitcode_file_path: 新附件本地路径
```

### 4.4. 向已有 release 上传多个附件（通过 release_id 定位）

```yaml
- name: Upload Multiple Assets to Existing Release by ID
  uses: nicennnnnnnlee/action-gitcode-release@master
  with:
    gitcode_action: upload_asset
    gitcode_owner: GitCode 用户名
    gitcode_repo: GitCode 项目名
    gitcode_token: ${{ secrets.gitcode_token }}
    gitcode_release_id: 12345
    gitcode_upload_retry_times: 3
    gitcode_files: |
      文件路径1
      文件路径2
```

### 5. 删除指定 tag 的 release

```yaml
- name: Delete Release
  uses: nicennnnnnnlee/action-gitcode-release@master
  with:
    gitcode_action: delete_release
    gitcode_owner: GitCode 用户名
    gitcode_repo: GitCode 项目名
    gitcode_token: ${{ secrets.gitcode_token }}
    gitcode_tag_name: v2.0.0
```

### 6.1. 删除 release 中的单个附件

```yaml
- name: Delete Single Asset
  uses: nicennnnnnnlee/action-gitcode-release@master
  with:
    gitcode_action: delete_asset
    gitcode_owner: GitCode 用户名
    gitcode_repo: GitCode 项目名
    gitcode_token: ${{ secrets.gitcode_token }}
    gitcode_tag_name: v2.0.0
    gitcode_delete_assets: 文件名
```

### 6.2. 删除 release 中的多个附件

```yaml
- name: Delete Multiple Assets
  uses: nicennnnnnnlee/action-gitcode-release@master
  with:
    gitcode_action: delete_asset
    gitcode_owner: GitCode 用户名
    gitcode_repo: GitCode 项目名
    gitcode_token: ${{ secrets.gitcode_token }}
    gitcode_tag_name: v2.0.0
    gitcode_delete_assets: |
      文件名1
      文件名2
      文件名3
```

### 7. 更新 release 中的附件

```yaml
- name: Update Asset
  uses: nicennnnnnnlee/action-gitcode-release@master
  with:
    gitcode_action: update_asset
    gitcode_owner: GitCode 用户名
    gitcode_repo: GitCode 项目名
    gitcode_token: ${{ secrets.gitcode_token }}
    gitcode_tag_name: v2.0.0
    gitcode_old_asset_name: 旧文件名称
    gitcode_new_file_path: 新文件本地路径
```

### 8. 使用 Action 输出的综合示例

```yaml
- name: Create Release and Use Output
  id: create_release
  uses: nicennnnnnnlee/action-gitcode-release@master
  with:
    gitcode_action: create_release
    gitcode_owner: GitCode 用户名
    gitcode_repo: GitCode 项目名
    gitcode_token: ${{ secrets.gitcode_token }}
    gitcode_tag_name: v2.0.0
    gitcode_release_name: Test v2.0.0
    gitcode_release_body: Release 描述
    gitcode_target_commitish: master

- name: Upload Additional Assets Using Release ID
  uses: nicennnnnnnlee/action-gitcode-release@master
  with:
    gitcode_action: upload_asset
    gitcode_owner: GitCode 用户名
    gitcode_repo: GitCode 项目名
    gitcode_token: ${{ secrets.gitcode_token }}
    gitcode_release_id: ${{ steps.create_release.outputs.release-id }}
    gitcode_files: |
      additional_file1.txt
      additional_file2.txt
```

## 参数说明

### 通用参数

- `gitcode_action`：执行的操作类型，可选值：`create_release`, `upload_asset`, `delete_release`, `delete_asset`, `update_asset`
- `gitcode_owner`：GitCode 用户名，项目 URL 中可获取
- `gitcode_repo`：GitCode 项目名，项目 URL 中可获取
- `gitcode_token`：GitCode api token
- `gitcode_tag_name`：GitCode Tag 名称，提倡以 v 字母为前缀做为 Release 名称，例如 v1.0 或者 v2.3.4

### create_release 专用参数

- `gitcode_release_name`：GitCode release 名称
- `gitcode_release_body`：GitCode release 描述
- `gitcode_target_commitish`：GitCode 分支名称或者 commit SHA

### 文件上传相关参数（create_release, upload_asset 可用）

- `gitcode_files`：上传的附件列表 (多个文件)。此处的文件路径支持规则匹配，参考[python-glob](https://docs.python.org/zh-cn/dev/library/glob.html)
- `gitcode_file_name`：上传的附件名称 (单个文件)
- `gitcode_file_path`：上传的附件的本地路径 (单个文件)
- `gitcode_release_id`：指定的 release ID (仅 upload_asset 操作时可用，如果指定则优先使用，否则通过 tag_name 查找)
- `gitcode_upload_retry_times`：上传附件失败后的尝试次数。默认为 0，不再尝试。

### delete_asset 专用参数

- `gitcode_delete_assets`：要删除的附件名称，每行一个文件名

### update_asset 专用参数

- `gitcode_old_asset_name`：要更新的旧附件名称
- `gitcode_new_file_path`：新附件的本地路径

## 输出说明

### create_release 操作输出

- `release-id`：创建的 release 的 ID，可用于后续的 upload_asset 操作

## 注意事项

- Token 需要以 [Secrets](https://docs.github.com/cn/actions/reference/encrypted-secrets) 方式给出，以保证 token 不被泄露
