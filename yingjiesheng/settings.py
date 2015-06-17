# -*- coding: utf-8 -*-

# Scrapy settings for yingjiesheng project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'yingjiesheng'

SPIDER_MODULES = ['yingjiesheng.spiders']
NEWSPIDER_MODULE = 'yingjiesheng.spiders'

COOKIES_ENABLED = False

ITEM_PIPELINES = {'yingjiesheng.pipelines.YingjieshengPipeline':300}

#取消默认的useragent,使用新的useragent
DOWNLOADER_MIDDLEWARES = {'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,'yingjiesheng.spiders.rotate_useragent.RotateUserAgentMiddleware' :400}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yingjiesheng (+http://www.yourdomain.com)'
