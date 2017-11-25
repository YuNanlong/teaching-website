# README

本仓库存储的是软件工程教学辅助网站的项目文件。

### 项目小组成员

石力铭 余南龙 叶金韬 张启锐 林洛舟 黄凯杰

**注意**

项目小组成员均已成为该仓库的collaborators，拥有该仓库的管理权限，但是在实际开发过程中请不要将自己的代码直接push到master分支上，请另外创建自己的分支并push到自己的分支上。

### 开发环境

+ Python版本3.6.0（本地3.5+都可以）
+ Django版本1.8.2（已经安装在虚拟环境中，Django1.8.2中文文档http://usyiyi.cn/translate/django_182/index.html）
+ MySQL5.6+（开发过程中本地数据库配置请见README中开发环境配置-数据库配置的部分）

**注明：**

如果在开发过程中使用了第三方库与工具，请在虚拟环境激活的情况下，使用：

```
cd 项目根目录
source venv/bin/activate
pip3 freeze > requirements.txt
```

将通过pip3安装的第三方库与工具的配置导入到requirements.txt文件中，以便小组其它成员通过以下方式安装：

```
cd 项目根目录
source venv/bin/activate
pip3 install -r requirements.txt
```

### 开发环境配置

**Python虚拟环境**

virtualenv虚拟环境的相关文件存储在venv目录下，激活虚拟环境：

```
source venv/bin/activate
```

**数据库配置**

```
mysql -u root -p #用root账户登录MySQL
create database teachingwebsite; #新建名为teachingwebsite的数据库
create user 'webadmin'@'localhost' identified by 'webadmin'; #新建名称和密码均为webadmin的用户
grant all privileges on teachingwebsite.* to 'webadmin'@'localhost'; #赋予webadmin用户对teachingwebsite数据库所有表的所有权限
quit; #退出root账户
```

