---
hide:
  - footer
---

<style>
  .md-typeset .grid.cards > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
    gap: 1rem;
    margin: 1em 0;
  }
  
  .md-typeset .grid.cards > ul > li {
    border: none;
    border-radius: 0.8rem;
    box-shadow: var(--md-shadow-z2);
    padding: 1.5rem;
    transition: transform 0.25s, box-shadow 0.25s;
    background: linear-gradient(135deg, var(--md-primary-fg-color), var(--md-accent-fg-color));
    color: var(--md-primary-bg-color);
  }

  .md-typeset .grid.cards > ul > li:hover {
    transform: scale(1.02);
    box-shadow: var(--md-shadow-z3);
  }

  .md-typeset .grid.cards > ul > li > hr {
    margin: 0.8rem 0;
    border: none;
    border-bottom: 2px solid var(--md-primary-bg-color);
    opacity: 0.2;
  }

  .md-typeset .grid.cards > ul > li > p {
    margin: 0.5rem 0;
  }

  .md-typeset .grid.cards > ul > li > p > em {
    color: var(--md-primary-bg-color);
    opacity: 0.8;
    font-style: normal;
  }

  .md-typeset .grid.cards > ul > li > p > .twemoji {
    font-size: 2.5rem;
    display: block;
    margin: 0.5rem auto;
  }

  .md-typeset .grid.cards > ul > li a {
    display: inline-block;
    padding: 0.4rem 1.2rem;
    margin-top: 0.6rem;
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 2rem;
    color: var(--md-primary-bg-color);
    font-weight: 500;
    transition: all 0.2s ease;
    text-decoration: none;
  }

  .md-typeset .grid.cards > ul > li a:hover {
    background-color: rgba(255, 255, 255, 0.3);
    transform: translateX(0.2rem);
  }

  .md-typeset .grid.cards > ul > li a::after {
    content: " →";
    opacity: 0;
    transition: opacity 0.2s ease;
  }

  .md-typeset .grid.cards > ul > li a:hover::after {
    opacity: 1;
  }
</style>

# 安装指南

## 🚀 部署方式

<div class="grid cards" markdown>

-   :material-docker:{ .twemoji }

    **Docker 部署**

    ---

    最简单的单机部署方式：
    
    - [查看教程 →](docker-installation.md)

-   :material-docker:{ .twemoji }

    **Docker Compose 部署**

    ---

    推荐的单机部署方式：
    
    - [查看教程 →](docker-compose-installation.md)

-   :material-server:{ .twemoji }

    **宝塔面板部署**

    ---

    使用宝塔面板进行可视化部署：
    
    - [查看教程 →](bt-docker-installation.md)

-   :material-server-network:{ .twemoji }

    **集群部署**

    ---

    大规模部署的最佳选择：
    
    - [查看教程 →](cluster-deployment.md)

</div>

## ⚙️ 配置与维护

<div class="grid cards" markdown>

-   :material-update:{ .twemoji }

    **系统更新**

    ---

    了解如何更新到最新版本：
    
    - [查看说明 →](system-update.md)

-   :material-variable:{ .twemoji }

    **环境变量**

    ---

    所有可配置的环境变量说明：
    
    - [查看文档 →](environment-variables.md)

-   :material-file-cog:{ .twemoji }

    **配置文件**

    ---

    Docker Compose 配置文件详解：
    
    - [查看说明 →](docker-compose-yml.md)

</div>

## 📖 部署说明

!!! tip "选择建议"
    - 个人用户建议使用 Docker 或 Docker Compose 部署
    - 熟悉宝塔面板的用户可以选择宝塔面板部署
    - 企业用户建议使用集群部署以获得更好的可扩展性

!!! warning "注意事项"
    部署前请确保：

    1. 已经安装了所需的基础软件
    2. 了解基本的 Linux 和 Docker 命令
    3. 服务器配置满足最低要求
    4. 已经准备好所需的API密钥

!!! info "获取帮助"
    如果在部署过程中遇到问题：

    1. 查看[常见问题](../support/faq.md)
    2. 在[GitHub](https://github.com/Calcium-Ion/new-api/issues)上提交issue
    3. 加入[QQ交流群](../support/community-interaction.md)寻求帮助 