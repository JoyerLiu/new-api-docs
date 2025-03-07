import os
import logging
from datetime import datetime
from github_api import fetch_github_data, GITHUB_REPO, GITHUB_PROXY, USE_PROXY
from afdian_api import fetch_afdian_sponsors
from utils import update_markdown_file, DOCS_DIR

logger = logging.getLogger('contributors')

def format_contributors_markdown(contributors_data):
    """将贡献者数据格式化为Markdown内容"""
    if not contributors_data or len(contributors_data) == 0:
        return "暂无贡献者数据，请稍后再试。"
    
    # 生成Markdown格式的贡献者列表
    markdown = ""
    
    # 为每个贡献者创建信息卡片
    for index, contributor in enumerate(contributors_data):
        username = contributor.get('login', '未知用户')
        avatar_url = contributor.get('avatar_url', '')
        # 替换头像URL为代理URL
        if USE_PROXY and 'githubusercontent.com' in avatar_url:
            avatar_url = f'{GITHUB_PROXY}?url={avatar_url}'
        profile_url = contributor.get('html_url', '')
        # 替换个人主页URL为代理URL
        if USE_PROXY and 'github.com' in profile_url:
            profile_url = f'{GITHUB_PROXY}?url={profile_url}'
        contributions = contributor.get('contributions', 0)
        
        # 获取前三名的特殊样式
        medal_class = ""
        medal_label = ""
        if index == 0:
            medal_class = "gold-medal"
            medal_label = '<span class="medal-rank rank-1">1</span>'
        elif index == 1:
            medal_class = "silver-medal"
            medal_label = '<span class="medal-rank rank-2">2</span>'
        elif index == 2:
            medal_class = "bronze-medal"
            medal_label = '<span class="medal-rank rank-3">3</span>'
        
        # 三级标题 + 简要介绍
        markdown += f'### {username}\n\n'
        markdown += f'<div class="contributor-simple {medal_class}">\n'
        markdown += f'  <div class="avatar-container">\n'
        markdown += f'    <img src="{avatar_url}" alt="{username}" class="contributor-avatar" />\n'
        if medal_label:
            markdown += f'    {medal_label}\n'
        markdown += f'  </div>\n'
        markdown += f'  <div class="contributor-details">\n'
        markdown += f'    <a href="{profile_url}" target="_blank">{username}</a>\n'
        markdown += f'    <span class="contributor-stats">贡献次数: {contributions}</span>\n'
        markdown += f'  </div>\n'
        markdown += f'</div>\n\n'
        markdown += '---\n\n'
    
    # 添加简洁的CSS样式
    markdown += '''
<style>
.contributor-simple {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.avatar-container {
    position: relative;
    margin-right: 15px;
}

.contributor-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
}

.medal-rank {
    position: absolute;
    bottom: -5px;
    right: -5px;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 12px;
    color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.rank-1 {
    background-color: #ffd700;
}

.rank-2 {
    background-color: #c0c0c0;
}

.rank-3 {
    background-color: #cd7f32;
}

.gold-medal .contributor-avatar {
    border: 4px solid #ffd700;
    box-shadow: 0 0 10px #ffd700;
}

.silver-medal .contributor-avatar {
    border: 4px solid #c0c0c0;
    box-shadow: 0 0 10px #c0c0c0;
}

.bronze-medal .contributor-avatar {
    border: 4px solid #cd7f32;
    box-shadow: 0 0 10px #cd7f32;
}

.contributor-details {
    display: flex;
    flex-direction: column;
}

.contributor-details a {
    font-weight: 500;
    text-decoration: none;
}

.contributor-stats {
    font-size: 0.9rem;
    color: #666;
}

[data-md-color-scheme="slate"] .contributor-stats {
    color: #aaa;
}
</style>
'''
    
    return markdown

def format_sponsors_markdown(sponsors_data):
    """将赞助商数据格式化为Markdown内容"""
    if not sponsors_data:
        return "暂无赞助商数据，请稍后再试。"
    
    # 生成Markdown格式的赞助商列表
    markdown = ""
    
    # 金牌赞助商
    gold_sponsors = sponsors_data.get('gold', [])
    if gold_sponsors:
        markdown += "### 🥇 金牌赞助商\n\n"
        markdown += "感谢以下金牌赞助商（赞助金额 ≥ 10001元）的慷慨支持！\n\n"
        
        for sponsor in gold_sponsors:
            name = sponsor.get('name', '匿名赞助者')
            avatar = sponsor.get('avatar', '')
            amount = sponsor.get('amount', 0)
            
            markdown += f'<div class="sponsor-card gold-sponsor">\n'
            markdown += f'  <div class="sponsor-avatar-container">\n'
            markdown += f'    <img src="{avatar}" alt="{name}" class="sponsor-avatar" />\n'
            markdown += f'    <span class="sponsor-medal gold-badge">金牌</span>\n'
            markdown += f'  </div>\n'
            markdown += f'  <div class="sponsor-details">\n'
            markdown += f'    <span class="sponsor-name">{name}</span>\n'
            markdown += f'    <span class="sponsor-amount">累计赞助: ¥{amount:.2f}</span>\n'
            markdown += f'  </div>\n'
            markdown += f'</div>\n\n'
        
        markdown += '---\n\n'
    
    # 银牌赞助商
    silver_sponsors = sponsors_data.get('silver', [])
    if silver_sponsors:
        markdown += "### 🥈 银牌赞助商\n\n"
        markdown += "感谢以下银牌赞助商（赞助金额 1001-10000元）的慷慨支持！\n\n"
        
        for sponsor in silver_sponsors:
            name = sponsor.get('name', '匿名赞助者')
            avatar = sponsor.get('avatar', '')
            amount = sponsor.get('amount', 0)
            
            markdown += f'<div class="sponsor-card silver-sponsor">\n'
            markdown += f'  <div class="sponsor-avatar-container">\n'
            markdown += f'    <img src="{avatar}" alt="{name}" class="sponsor-avatar" />\n'
            markdown += f'    <span class="sponsor-medal silver-badge">银牌</span>\n'
            markdown += f'  </div>\n'
            markdown += f'  <div class="sponsor-details">\n'
            markdown += f'    <span class="sponsor-name">{name}</span>\n'
            markdown += f'    <span class="sponsor-amount">累计赞助: ¥{amount:.2f}</span>\n'
            markdown += f'  </div>\n'
            markdown += f'</div>\n\n'
        
        markdown += '---\n\n'
    
    # 铜牌赞助商
    bronze_sponsors = sponsors_data.get('bronze', [])
    if bronze_sponsors:
        markdown += "### 🥉 铜牌赞助商\n\n"
        markdown += "感谢以下铜牌赞助商（赞助金额 0-1000元）的支持！\n\n"
        
        # 为铜牌赞助商创建网格布局
        markdown += '<div class="bronze-sponsors-grid">\n'
        
        for sponsor in bronze_sponsors:
            name = sponsor.get('name', '匿名赞助者')
            avatar = sponsor.get('avatar', '')
            amount = sponsor.get('amount', 0)
            
            markdown += f'  <div class="bronze-sponsor-item">\n'
            markdown += f'    <img src="{avatar}" alt="{name}" class="sponsor-avatar-small" />\n'
            markdown += f'    <span class="bronze-sponsor-name">{name}</span>\n'
            markdown += f'    <span class="bronze-sponsor-amount">¥{amount:.2f}</span>\n'
            markdown += f'  </div>\n'
        
        markdown += '</div>\n\n'
        markdown += '---\n\n'
    
    # 添加赞助商CSS样式
    markdown += '''
<style>
.sponsor-card {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(0,0,0,0.03);
}

[data-md-color-scheme="slate"] .sponsor-card {
    background-color: rgba(255,255,255,0.05);
}

.sponsor-avatar-container {
    position: relative;
    margin-right: 20px;
}

.sponsor-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
}

.sponsor-medal {
    position: absolute;
    bottom: -5px;
    right: -5px;
    padding: 3px 8px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: bold;
    color: white;
}

.gold-badge {
    background-color: #ffd700;
    color: #333;
}

.silver-badge {
    background-color: #c0c0c0;
    color: #333;
}

.bronze-badge {
    background-color: #cd7f32;
    color: white;
}

.gold-sponsor .sponsor-avatar {
    border: 4px solid #ffd700;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.silver-sponsor .sponsor-avatar {
    border: 4px solid #c0c0c0;
    box-shadow: 0 0 10px rgba(192, 192, 192, 0.5);
}

.sponsor-details {
    display: flex;
    flex-direction: column;
}

.sponsor-name {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 5px;
}

.sponsor-amount {
    font-size: 0.9rem;
    color: #666;
}

[data-md-color-scheme="slate"] .sponsor-amount {
    color: #aaa;
}

.bronze-sponsors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
}

.bronze-sponsor-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    background-color: rgba(0,0,0,0.02);
}

[data-md-color-scheme="slate"] .bronze-sponsor-item {
    background-color: rgba(255,255,255,0.03);
}

.sponsor-avatar-small {
    width: 50px !important;
    height: 50px !important;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #cd7f32;
    margin-bottom: 8px;
}

.bronze-sponsor-name {
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 4px;
    word-break: break-word;
}

.bronze-sponsor-amount {
    font-size: 0.8rem;
    color: #666;
}

[data-md-color-scheme="slate"] .bronze-sponsor-amount {
    color: #aaa;
}
</style>
'''
    
    return markdown

def update_special_thanks_file():
    """更新特别感谢文件"""
    try:
        # 获取贡献者数据
        contributors_data, contributors_success = fetch_github_data(GITHUB_REPO, "contributors", 50)
        
        # 获取赞助商数据
        sponsors_data, sponsors_success = fetch_afdian_sponsors()
        
        # 如果两者都失败，则返回失败
        if not contributors_success and not sponsors_success:
            logger.error("无法获取贡献者和赞助商数据")
            return False
        
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 格式化基础内容
        base_content = f"""# 🙏特别鸣谢\n\n

New API 的开发离不开社区的支持和贡献。在此特别感谢所有为项目提供帮助的个人和组织。

"""
        
        # 添加赞助商部分
        sponsors_content = ""
        if sponsors_success and sponsors_data:
            sponsors_content = f"""## ❤️赞助商

以下是所有为项目提供资金支持的赞助商。感谢他们的慷慨捐助，让项目能够持续发展！

!!! info "赞助商信息（数据更新于: {current_time}）"
    以下赞助商数据从爱发电平台自动获取。根据累计赞助金额，分为金牌、银牌和铜牌三个等级。
    如果您也想为项目提供资金支持，欢迎前往 [爱发电](https://afdian.com/a/new-api) 平台进行捐赠。

{format_sponsors_markdown(sponsors_data)}
"""
        
        # 添加开发者部分
        developers_content = ""
        if contributors_success and contributors_data:
            developers_content = f"""## 👨‍💻 开发贡献者

以下是所有为项目做出贡献的开发者列表。在此感谢他们的辛勤工作和创意！

!!! info "贡献者信息 · 数据更新于 {current_time}）"
    以下贡献者数据从 [GitHub Contributors 页面](https://github.com/Calcium-Ion/new-api/graphs/contributors) 自动获取前50名。贡献度前三名分别以金、银、铜牌边框标识。如果您也想为项目做出贡献，欢迎提交 Pull Request。

{format_contributors_markdown(contributors_data)}
"""
        
        # 组合完整内容
        full_content = base_content + sponsors_content + developers_content
        
        # 更新文件
        thanks_file = os.path.join(DOCS_DIR, 'docs/wiki/special-thanks.md')
        return update_markdown_file(thanks_file, full_content)
    
    except Exception as e:
        logger.error(f"更新贡献者列表失败: {str(e)}")
        return False