from scrapy.commands import ScrapyCommand
from weixin_scrapy.verifycode import handel_verifycode

class Command(ScrapyCommand):
    def short_desc(self):
        return "处理验证码输入"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("-u", "--url", help="需要验证的url")
        parser.add_option("-t", "--type", help="验证网站类型")

    def run(self, args, opts):
        handel_verifycode(*args)
