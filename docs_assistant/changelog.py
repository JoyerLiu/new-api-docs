import os
import re
import logging
from datetime import datetime
from github_api import fetch_github_data, GITHUB_REPO, GITHUB_PROXY, USE_PROXY
from utils import update_markdown_file, format_file_size, DOCS_DIR

logger = logging.getLogger('changelog')

def format_releases_markdown(releases_data):
    """将发布数据格式化为Markdown内容"""
    if not releases_data or len(releases_data) == 0:
        return "暂无版本数据，请稍后再试。"
    
    markdown = "# 📝 更新日志\n\n"
    
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    markdown += "!!! warning \"更多版本\"\n"
    markdown += f"    如需查看全部历史版本，请访问 [GitHub Releases 页面](https://github.com/{GITHUB_REPO}/releases)，本页面从该页面定时获取最新更新信息。\n"
    markdown += f"    数据更新于: {current_time}\n\n"
    
    for index, release in enumerate(releases_data):
        tag_name = release.get('tag_name', '未知版本')
        name = release.get('name') or tag_name
        published_at = release.get('published_at', '')
        body = release.get('body', '无发布说明')
        prerelease = release.get('prerelease', False)
        
        if published_at:
            try:
                # 转换ISO格式的时间为更友好的格式
                pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                formatted_date = pub_date.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                formatted_date = published_at
        else:
            formatted_date = '未知时间'
        
        # 处理Markdown格式
        body = body.replace('### ', '#### ').replace('## ', '### ')
        
        # 替换图片链接（如果使用代理）
        if USE_PROXY:
            # 替换Markdown格式的图片链接
            body = re.sub(r'!\[(.*?)\]\((https?://[^)]+)\)', 
                          f'![\g<1>]({GITHUB_PROXY}?url=\\2)', 
                          body)
            
            # 替换HTML格式的图片链接
            body = re.sub(r'<img([^>]*)src="(https?://[^"]+)"([^>]*)>', 
                          f'<img\\1src="{GITHUB_PROXY}?url=\\2"\\3>', 
                          body)
        
        markdown += f'## {name}\n\n'
        
        # 版本类型标签
        version_type = "预发布版本" if prerelease else "正式版本"
        if index == 0:
            version_type = f"最新{version_type}"
            admonition_type = "success"
        else:
            admonition_type = "info"
        
        markdown += f'???+ {admonition_type} "{version_type} · 发布于 {formatted_date}"\n\n'
        
        # 缩进内容以适应admonition格式
        indented_body = '\n'.join(['    ' + line for line in body.split('\n')])
        markdown += f'{indented_body}\n\n'
        
        # 添加资源下载部分
        assets = release.get('assets', [])
        if assets or tag_name:
            markdown += '    **下载资源**\n\n'
            # 添加正常资源
            for asset in assets:
                name = asset.get('name', '')
                url = asset.get('browser_download_url', '')
                # 替换下载URL为代理URL
                if USE_PROXY and 'github.com' in url:
                    url = f'{GITHUB_PROXY}?url={url}'
                size = format_file_size(asset.get('size', 0))
                markdown += f'    - [{name}]({url}) ({size})\n'
            
            # 添加源代码下载链接
            if tag_name:
                # 构建zip下载链接
                zip_url = f'https://github.com/{GITHUB_REPO}/archive/refs/tags/{tag_name}.zip'
                if USE_PROXY:
                    proxy_zip_url = f'{GITHUB_PROXY}?url={zip_url}'
                    markdown += f'    - [Source code (zip)]({proxy_zip_url})\n'
                else:
                    markdown += f'    - [Source code (zip)]({zip_url})\n'
                
                # 构建tar.gz下载链接
                tar_url = f'https://github.com/{GITHUB_REPO}/archive/refs/tags/{tag_name}.tar.gz'
                if USE_PROXY:
                    proxy_tar_url = f'{GITHUB_PROXY}?url={tar_url}'
                    markdown += f'    - [Source code (tar.gz)]({proxy_tar_url})\n'
                else:
                    markdown += f'    - [Source code (tar.gz)]({tar_url})\n'
            
            markdown += '\n'
        
        markdown += '---\n\n'
    
    return markdown

def update_changelog_file():
    """更新更新日志文件"""
    try:
        # 获取发布数据
        releases_data, success = fetch_github_data(GITHUB_REPO, "releases", 30)
        if not success or not releases_data:
            logger.error("无法获取发布数据")
            return False
        
        # 格式化为Markdown
        releases_markdown = format_releases_markdown(releases_data)
        
        # 更新到文件
        changelog_file = os.path.join(DOCS_DIR, 'docs/wiki/changelog.md')
        return update_markdown_file(changelog_file, releases_markdown)
    
    except Exception as e:
        logger.error(f"更新更新日志失败: {str(e)}")
        return False