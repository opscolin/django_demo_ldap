
## 1、安装Ldap 和 phpldapadmin 

使用 docker-ldap 下面的 docker-compose.yml 启动一个 ldap服务及ldap管控界面

注意端口

+ 389端口，默认的LDAP端，支持TCP/UDP传输
+ 636端口是支持SSL/TLS 上的 LDAP
+ 80端口是phpldapadmin的web端口，用于管控ldap

使用 `docker-compose` 命令启动

```bash
cd docker-ldap
# 后台启动
docker-compose up -d
```

启动之后的打开 phpldapadmin管理界面，账号是 `cn=admin,dc=colinspace,dc=com` 密码是配置的`colinXXLdap`具体看自己的配置值， 看是否可以登录成功


## 2、克隆项目并做初始化

```bash
# 下载 

git clone 

cd django_demo_ldap
# 先初始化库
python manage.py makemigrations
python manage.py migrate

# 创建管理员账号密码 （注意这里的管理员密码可以不和Ldap的Admin的密码一致）
python manage.py createsuperuser

# 然后启动Django服务
python manage.py runserver 0.0.0.0:8082 
```

使用创建的管理员账号密码尝试登录 Django后台是否可以正常登录



## 3、在phpldapadmin后台新增用户

ldap admin登录成功之后，在右侧 `dc=colinspace,dc=com` 下点击`Create new entry here`

如果初次登录之后没有的话，点击选中右侧 `dc=colinspace,dc=com`，然后在页面左边会有`Create new entry here`

通过Ldap新增用户时

1、选择`Templates`为 `Default`

2、选择 `ObjectClasses` 的值为 `inetOrgPerson` （Django项目中配置的这个）然后下一步

3、这一步的关键

    3.1、顶部的`RDN` 选择 `cn（cn）`

    3.2、然后cn选项就是我们登录Django的用户名

    3.3、然后sn也是必选项，对应Django的 `last name`

    3.4、然后可选的配置`displayName`和`Mobile`、 `Email` （邮箱强烈建议填上）

    3.5、最后在配置`Password` 密码，这个密码可用登录ldap，也是登录Django后台的

    3.6、然后下一步，最终确认创建


## 4、使用ldap创建账号登录Django后台

默认登录是报错，提示如下

```bash
Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.
```

但是使用 admin 登录Django后台看到实际是创建了对应的Django用户，但是`is_staff`状态是`false`

这个时候，你可以在Django后台手动修改这个状态，然后再次登录就没有问题了。

## 5、通过Django信号机制优化初次登录的报错

这里可以在Django app中新增signals.py文件，具体内容详见源码，然后在 APP的 `apps.py`中添加如下配置

```python
from django.apps import AppConfig


class DemoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'demoapp'
    
    # 新增如下两行配置
    def ready(self):
        import demoapp.signals
```

下次新增ldap账号之后，再用新的账号登录Django后台时就不会报错，因为这个时候自动新增的Django用户的is_staff就是`True` 状态了。
