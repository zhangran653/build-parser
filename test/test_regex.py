import json
import unittest

from regex.ASTPrinter import ASTPrinter
from regex.Parser import Parser
from regex.Scanner import Scanner


class RegexTest(unittest.TestCase):
    def test1(self):
        scanner = Scanner('')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test2(self):
        scanner = Scanner('a')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test3(self):
        scanner = Scanner('ab+')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test4(self):
        scanner = Scanner('[]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test5(self):
        scanner = Scanner('[a-zA-Z]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test6(self):
        scanner = Scanner('[a-zA-Z\[]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test7(self):
        scanner = Scanner('a{3,4}')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test8(self):
        scanner = Scanner('ad阿松大')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test9(self):
        scanner = Scanner('\s\\b\w\S\A\Z\G.|')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test10(self):
        scanner = Scanner("")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expressions = parser.parse()
        print(expressions)

    def test11(self):
        """
        1. 数字：^[0-9]*$
        2. n位的数字：^\d{n}$
        3. 至少n位的数字：^\d{n,}$
        4. m-n位的数字：^\d{m,n}$
        5. 零和非零开头的数字：^(0|[1-9][0-9]*)$
        6. 非零开头的最多带两位小数的数字：^([1-9][0-9]*)+(.[0-9]{1,2})?$
        7. 带1-2位小数的正数或负数：^(\-)?\d+(\.\d{1,2})?$
        8. 正数、负数、和小数：^(\-|\+)?\d+(\.\d+)?$
        9. 有两位小数的正实数：^[0-9]+(.[0-9]{2})?$
        10. 有1~3位小数的正实数：^[0-9]+(.[0-9]{1,3})?$
        11. 非零的正整数：^[1-9]\d*$ 或 ^([1-9][0-9]*){1,3}$ 或 ^\+?[1-9][0-9]*$
        12. 非零的负整数：^\-[1-9][]0-9"*$ 或 ^-[1-9]\d*$
        13. 非负整数：^\d+$ 或 ^[1-9]\d*|0$
        14. 非正整数：^-[1-9]\d*|0$ 或 ^((-\d+)|(0+))$
        15. 非负浮点数：^\d+(\.\d+)?$ 或 ^[1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0$
        16. 非正浮点数：^((-\d+(\.\d+)?)|(0+(\.0+)?))$ 或 ^(-([1-9]\d*\.\d*|0\.\d*[1-9]\d*))|0?\.0+|0$
        17. 正浮点数：^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$ 或 ^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$
        18. 负浮点数：^-([1-9]\d*\.\d*|0\.\d*[1-9]\d*)$ 或 ^(-(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*)))$
        19. 浮点数：^(-?\d+)(\.\d+)?$ 或 ^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$

        :return:
        """
        regexes = [
            "^[0-9]*$",
            "^\\d{4}$",
            "^\\d{5,}$",
            "^\\d{3,6}$",
            "^(0|[1-9][0-9]*)$",
            "^([1-9][0-9]*)+(.[0-9]{1,2})?$",
            "^(\\-)?\\d+(\\.\\d{1,2})?$",
            "^(\\-|\\+)?\\d+(\\.\\d+)?$",
            "^[0-9]+(.[0-9]{2})?$",
            "^[0-9]+(.[0-9]{1,3})?$",
            "^[1-9]\\d*$",
            "^([1-9][0-9]*){1,3}$",
            "^\\+?[1-9][0-9]*$",
            "^\\-[1-9][0-9]*$",
            "^-[1-9]\\d*$",
            "^\\d+$",
            "^[1-9]\\d*|0$",
            "^-[1-9]\\d*|0$",
            "^((-\\d+)|(0+))$",
            "^\\d+(\\.\\d+)?$",
            "^[1-9]\\d*\\.\\d*|0\\.\\d*[1-9]\\d*|0?\\.0+|0$",
            "^((-\\d+(\\.\\d+)?)|(0+(\\.0+)?))$",
            "^(-([1-9]\\d*\\.\\d*|0\\.\\d*[1-9]\\d*))|0?\\.0+|0$",
            "^[1-9]\\d*\\.\\d*|0\\.\\d*[1-9]\\d*$",
            "^(([0-9]+\\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\\.[0-9]+)|([0-9]*[1-9][0-9]*))$",
            "^-([1-9]\\d*\\.\\d*|0\\.\\d*[1-9]\\d*)$",
            "^(-(([0-9]+\\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\\.[0-9]+)|([0-9]*[1-9][0-9]*)))$",
            "^(-?\\d+)(\\.\\d+)?$",
            "^-?([1-9]\\d*\\.\\d*|0\\.\\d*[1-9]\\d*|0?\\.0+|0)$",
            "^[\u4e00-\u9fa5]{0,}$"
        ]
        for r in regexes:
            print("====")
            print(f"{r}")
            print(':')
            scanner = Scanner(r)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expressions = parser.parse()
            printer = ASTPrinter()
            ret = printer.ast_string(expressions)
            # Parse the JSON string into a Python dictionary
            parsed_json = json.loads(ret)
            # Pretty print the JSON
            pretty_json = json.dumps(parsed_json, indent=2)
            print(pretty_json)
            print("====")
            print()

    def test12(self):
        """
        1. 汉字：^[\u4e00-\u9fa5]{0,}$
        2. 英文和数字：^[A-Za-z0-9]+$ 或 ^[A-Za-z0-9]{4,40}$
        3. 长度为3-20的所有字符：^.{3,20}$
        4. 由26个英文字母组成的字符串：^[A-Za-z]+$
        5. 由26个大写英文字母组成的字符串：^[A-Z]+$
        6. 由26个小写英文字母组成的字符串：^[a-z]+$
        7. 由数字和26个英文字母组成的字符串：^[A-Za-z0-9]+$
        8. 由数字、26个英文字母或者下划线组成的字符串：^\w+$ 或 ^\w{3,20}$
        9. 中文、英文、数字包括下划线：^[\u4E00-\u9FA5A-Za-z0-9_]+$
        10. 中文、英文、数字但不包括下划线等符号：^[\u4E00-\u9FA5A-Za-z0-9]+$ 或 ^[\u4E00-\u9FA5A-Za-z0-9]{2,20}$
        11. 可以输入含有^%&',;=?$\"等字符：[^%&',;=?$\x22]+ 12 禁止输入含有~的字符：[^~\x22]+
        :return:
        """
        regexes = [
            "^[\u4e00-\u9fa5]{0,}$",
            "^[A-Za-z0-9]+$",
            "^[A-Za-z0-9]{4,40}$",
            "^.{3,20}$",
            "^[A-Za-z]+$",
            "^[A-Z]+$",
            "^[a-z]+$",
            "^[A-Za-z0-9]+$",
            "^\\w+$", "^\\w{3,20}$",
            "^[\u4E00-\u9FA5A-Za-z0-9_]+$",
            "^[\u4E00-\u9FA5A-Za-z0-9]+$",
            "^[\u4E00-\u9FA5A-Za-z0-9]{2,20}$",
        ]
        for r in regexes:
            print("====")
            print(f"{r}")
            print(':')
            scanner = Scanner(r)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expressions = parser.parse()
            printer = ASTPrinter()
            ret = printer.ast_string(expressions)
            # Parse the JSON string into a Python dictionary
            parsed_json = json.loads(ret)
            # Pretty print the JSON
            pretty_json = json.dumps(parsed_json, indent=2)
            print(pretty_json)
            print("====")
            print()

    def test13(self):
        """
        1. Email地址：^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$
        2. 域名：[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/.?
        3. InternetURL：[a-zA-z]+://[^\s]* 或 ^http://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$
        4. 手机号码：^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$
        5. 电话号码("XXX-XXXXXXX"、"XXXX-XXXXXXXX"、"XXX-XXXXXXX"、"XXX-XXXXXXXX"、"XXXXXXX"和"XXXXXXXX)：^(\(\d{3,4}-)|\d{3.4}-)?\d{7,8}$
        6. 国内电话号码(0511-4405222、021-87888822)：\d{3}-\d{8}|\d{4}-\d{7}
        7. 身份证号(15位、18位数字)：^\d{15}|\d{18}$
        :return:
        """
        regexes = [
            "^\\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",

        ]
        for r in regexes:
            print("====")
            print(f"{r}")
            print(':')
            scanner = Scanner(r)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expressions = parser.parse()
            printer = ASTPrinter()
            ret = printer.ast_string(expressions)
            # Parse the JSON string into a Python dictionary
            parsed_json = json.loads(ret)
            # Pretty print the JSON
            pretty_json = json.dumps(parsed_json, indent=2)
            print(pretty_json)
            print("====")
            print()