import json
import unittest

from regex.ASTPrinter import ASTPrinter
from regex.EngineNFA import EngineNFA
from regex.NFAMatcher import CharacterMatcher, EpsilonMatcher
from regex.NFARegex import NFARegex
from regex.Parser import Parser
from regex.Scanner import Scanner


class RegexTest(unittest.TestCase):
    def test0(self):
        s = r'\\['
        print(f"len :{len(s)}")
        for i in range(0, len(s)):
            print(s[i])

    def test1(self):
        scanner = Scanner(r'')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test2(self):
        scanner = Scanner(r'a')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test3(self):
        scanner = Scanner(r'ab+')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test4(self):
        scanner = Scanner(r'[]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test5(self):
        scanner = Scanner(r'[a-zA-Z]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test6(self):
        scanner = Scanner(r'[a-zA-Z\[]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test7(self):
        scanner = Scanner(r'a{3,4}')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test8(self):
        scanner = Scanner(r'ad阿松大')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test9(self):
        scanner = Scanner(r'\s\\b\w\S\A\Z\G.|')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test10(self):
        scanner = Scanner(r"")
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
            r"^[0-9]*$",
            r"^\d{4}$",
            r"^\d{5,}$",
            r"^\d{3,6}$",
            r"^(0|[1-9][0-9]*)$",
            r"^([1-9][0-9]*)+(.[0-9]{1,2})?$",
            r"^(\-)?\d+(\.\d{1,2})?$",
            r"^(\-|\+)?\d+(\.\d+)?$",
            r"^[0-9]+(.[0-9]{2})?$",
            r"^[0-9]+(.[0-9]{1,3})?$",
            r"^[1-9]\d*$",
            r"^([1-9][0-9]*){1,3}$",
            r"^\+?[1-9][0-9]*$",
            r"^\-[1-9][0-9]*$",
            r"^-[1-9]\d*$",
            r"^\d+$",
            r"^[1-9]\d*|0$",
            r"^-[1-9]\d*|0$",
            r"^((-\d+)|(0+))$",
            r"^\d+(\.\d+)?$",
            r"^[1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0$",
            r"^((-\d+(\.\d+)?)|(0+(\.0+)?))$",
            r"^(-([1-9]\d*\.\d*|0\.\d*[1-9]\d*))|0?\.0+|0$",
            r"^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$",
            r"^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$",
            r"^-([1-9]\d*\.\d*|0\.\d*[1-9]\d*)$",
            r"^(-(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*)))$",
            r"^(-?\d+)(\.\d+)?$",
            r"^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$",
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
            r"^[A-Za-z0-9]+$",
            r"^[A-Za-z0-9]{4,40}$",
            r"^.{3,20}$",
            r"^[A-Za-z]+$",
            r"^[A-Z]+$",
            r"^[a-z]+$",
            r"^[A-Za-z0-9]+$",
            r"^\w+$", "^\w{3,20}$",
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
        8 短身份证号码(数字、字母x结尾)：^([0-9]){7,18}(x|X)?$ 或 ^\d{8,18}|[0-9x]{8,18}|[0-9X]{8,18}?$
        9 帐号是否合法(字母开头，允许5-16字节，允许字母数字下划线)：^[a-zA-Z][a-zA-Z0-9_]{4,15}$
        10 密码(以字母开头，长度在6~18之间，只能包含字母、数字和下划线)：^[a-zA-Z]\w{5,17}$
        11 强密码(必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-10之间)：^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$
        12 日期格式：^\d{4}-\d{1,2}-\d{1,2}
        13 一年的12个月(01～09和1～12)：^(0?[1-9]|1[0-2])$
        14 一个月的31天(01～09和1～31)：^((0?[1-9])|((1|2)[0-9])|30|31)$
        15 钱的输入格式：
        16 1.有四种钱的表示形式我们可以接受:"10000.00" 和 "10,000.00", 和没有 "分" 的 "10000" 和 "10,000"：^[1-9][0-9]*$
        17 2.这表示任意一个不以0开头的数字,但是,这也意味着一个字符"0"不通过,所以我们采用下面的形式：^(0|[1-9][0-9]*)$
        18 3.一个0或者一个不以0开头的数字.我们还可以允许开头有一个负号：^(0|-?[1-9][0-9]*)$
        19 4.这表示一个0或者一个可能为负的开头不为0的数字.让用户以0开头好了.把负号的也去掉,因为钱总不能是负的吧.下面我们要加的是说明可能的小数部分：^[0-9]+(.[0-9]+)?$
        20 5.必须说明的是,小数点后面至少应该有1位数,所以"10."是不通过的,但是 "10" 和 "10.2" 是通过的：^[0-9]+(.[0-9]{2})?$
        21 6.这样我们规定小数点后面必须有两位,如果你认为太苛刻了,可以这样：^[0-9]+(.[0-9]{1,2})?$
        22 7.这样就允许用户只写一位小数.下面我们该考虑数字中的逗号了,我们可以这样：^[0-9]{1,3}(,[0-9]{3})*(.[0-9]{1,2})?$
        23 8.1到3个数字,后面跟着任意个 逗号+3个数字,逗号成为可选,而不是必须：^([0-9]+|[0-9]{1,3}(,[0-9]{3})*)(.[0-9]{1,2})?$
        24 备注：这就是最终结果了,别忘了"+"可以用"*"替代如果你觉得空字符串也可以接受的话(奇怪,为什么?)最后,别忘了在用函数时去掉去掉那个反斜杠,一般的错误都在这里
        25 xml文件：^([a-zA-Z]+-?)+[a-zA-Z0-9]+\\.[x|X][m|M][l|L]$
        26 中文字符的正则表达式：[\u4e00-\u9fa5]
        27 双字节字符：[^\x00-\xff] (包括汉字在内，可以用来计算字符串的长度(一个双字节字符长度计2，ASCII字符计1))
        28 空白行的正则表达式：\n\s*\r (可以用来删除空白行)
        29 HTML标记的正则表达式：<(\S*?)[^>]*>.*?</\1>|<.*? /> (网上流传的版本太糟糕，上面这个也仅仅能部分，对于复杂的嵌套标记依旧无能为力)
        30 首尾空白字符的正则表达式：^\s*|\s*$或(^\s*)|(\s*$) (可以用来删除行首行尾的空白字符(包括空格、制表符、换页符等等)，非常有用的表达式)
        31 腾讯QQ号：[1-9][0-9]{4,} (腾讯QQ号从10000开始)
        32 中国邮政编码：[1-9]\d{5}(?!\d) (中国邮政编码为6位数字) 33 IP地址：\d+\.\d+\.\d+\.\d+ (提取IP地址时有用) 34 IP地址：((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))
        :return:
        """
        regexes = [
            r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
            r"[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/.?",
            r"^http://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$",
            r"[a-zA-z]+://[^\s]*",
            r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$",
            r"^(\d{3,4}-)|(\d{3,4}-)?\d{7,8}$",
            r"\d{3}-\d{8}|\d{4}-\d{7}",
            r"^\d{15}|\d{18}$",
            r"^([0-9]){7,18}(x|X)?$",
            r"\d{8,18}|[0-9x]{8,18}|[0-9X]{8,18}?$",
            r"^\s*|\s*$",
            r"(^\s*)|(\s*$)",
            r"^(\d{1,4})(-|\\/)(\d{1,2})\\2(\d{1,2})$"
        ]
        for r in regexes:
            print("====")
            print(f"{r}, len:{len(r)}")
            print(':')
            scanner = Scanner(r)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expressions = parser.parse()
            printer = ASTPrinter()
            ret = printer.ast_string(expressions)
            # print(ret)
            # Parse the JSON string into a Python dictionary
            parsed_json = json.loads(ret)
            # Pretty print the JSON
            pretty_json = json.dumps(parsed_json, indent=2)
            print(pretty_json)
            print("====")
            print()

    def test14(self):
        regexes = [
            r"[\w-a-z]",
            r"[a-zA-Z]",
            r"<(.+?)>",
            r"<([^>]+?)>"
            r"a",
        ]
        for r in regexes:
            print("====")
            print(f"{r}, len:{len(r)}")
            print(':')
            scanner = Scanner(r)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expressions = parser.parse()
            printer = ASTPrinter()
            ret = printer.ast_string(expressions)
            # print(ret)
            # Parse the JSON string into a Python dictionary
            parsed_json = json.loads(ret)
            # Pretty print the JSON
            pretty_json = json.dumps(parsed_json, indent=2)
            print(pretty_json)
            print("====")
            print()

    def test15(self):
        nfa = EngineNFA()
        nfa.add_states("q0", "q1", "q2", "q3")
        nfa.initial_state = "q0"
        nfa.ending_states = ["q2"]

        """                -b-
                          \  /
           q0 -a-> q1 -b-> q2 -eps-> q3
        
        """
        nfa.add_transition("q0", "q1", CharacterMatcher("a"))
        nfa.add_transition("q1", "q2", CharacterMatcher("b"))
        nfa.add_transition("q2", "q2", CharacterMatcher("b"))
        nfa.add_transition("q2", "q3", EpsilonMatcher())

        print(nfa.compute("abbbb"))
        print(nfa.compute("aabbbb"))
        print(nfa.compute("ab"))
        print(nfa.compute("a"))

    def test16(self):
        nfa = EngineNFA()
        nfa.add_states("q0", "q1", "q2")
        nfa.initial_state = "q0"
        nfa.ending_states = ["q2"]
        """                
                         \^ε^/       
                   q0 -a-> q1 -b-> q2

        """
        nfa.add_transition("q0", "q1", CharacterMatcher("a"))
        nfa.add_transition("q1", "q1", EpsilonMatcher())
        nfa.add_transition("q1", "q2", CharacterMatcher("b"))
        print(nfa.compute("abc"))

    def print_groups(self, nfa: NFARegex):
        for k, v in nfa.groups.items():
            print(v)

    def test17(self):
        nfa = NFARegex(r"(?<g1>a|b)+c*")
        printer = ASTPrinter()
        ret = printer.ast_string(nfa.ast)
        print(ret)
        # Parse the JSON string into a Python dictionary
        parsed_json = json.loads(ret)
        # Pretty print the JSON
        pretty_json = json.dumps(parsed_json, indent=2)
        print(pretty_json)

        assert nfa.compute("abababababacccc")
        self.print_groups(nfa)
        assert not nfa.compute("caaaabbbab")
        self.print_groups(nfa)
        assert nfa.compute("bb")
        self.print_groups(nfa)
        assert nfa.compute("aaaaaaa")
        self.print_groups(nfa)
        assert nfa.compute("a")
        self.print_groups(nfa)
        assert nfa.compute("b")
        self.print_groups(nfa)
        assert nfa.compute("bbbbbb")
        self.print_groups(nfa)
        assert nfa.compute("ab")
        self.print_groups(nfa)
        assert nfa.compute("ba")
        self.print_groups(nfa)
        assert nfa.compute("ac")
        self.print_groups(nfa)
        assert nfa.compute("acccc")
        self.print_groups(nfa)
        assert nfa.compute("bc")
        self.print_groups(nfa)
        assert nfa.compute("bcccc")
        self.print_groups(nfa)
        assert not nfa.compute("c")
        self.print_groups(nfa)
        assert not nfa.compute("ca")
        self.print_groups(nfa)
        assert not nfa.compute("cb")
        self.print_groups(nfa)
        assert not nfa.compute("x")
        self.print_groups(nfa)

    def test18(self):
        nfa = NFARegex("a+c?b+")
        printer = ASTPrinter()
        ret = printer.ast_string(nfa.ast)
        # print(ret)
        # Parse the JSON string into a Python dictionary
        parsed_json = json.loads(ret)
        # Pretty print the JSON
        pretty_json = json.dumps(parsed_json, indent=2)
        print(pretty_json)

        assert nfa.compute("aaaaacbbbbbb")
        self.print_groups(nfa)
        assert not nfa.compute("accb")
        self.print_groups(nfa)
        assert nfa.compute("ab")
        self.print_groups(nfa)
        assert nfa.compute("aabb")
        self.print_groups(nfa)
        assert nfa.compute("aacbb")
        self.print_groups(nfa)
        assert not nfa.compute("cb")
        self.print_groups(nfa)

    def test19(self):
        nfa = NFARegex("(?<g1>a|b)+c")

        assert not nfa.compute("a")
        self.print_groups(nfa)
        assert nfa.compute("ac")
        self.print_groups(nfa)
        assert not nfa.compute("c")
        self.print_groups(nfa)

    def test20(self):
        nfa = NFARegex("((?:a|b)+(x(1|2(z))))(cd)")
        assert nfa.compute("aabbx1cd")
        self.print_groups(nfa)

    def test21(self):
        nfa = NFARegex("(?<ga>a+)(?<gb>b+)")
        assert nfa.compute("aaabb")
        self.print_groups(nfa)

    def test22(self):
        nfa = NFARegex("\n")
        assert nfa.compute("\n")
        self.print_groups(nfa)

        nfa = NFARegex("\++\w+")
        assert nfa.compute("+++++123df")
        self.print_groups(nfa)

    def test23(self):
        nfa = NFARegex("[0-8]+")
        assert nfa.find("asd0123456789asdfa123")
        self.print_groups(nfa)
        nfa = NFARegex("[^0-8]+")
        assert nfa.compute("aeaa119abcde102a")
        self.print_groups(nfa)

        nfa = NFARegex("[\d]+")
        assert nfa.compute("1234100123410412346899")
        self.print_groups(nfa)

        nfa = NFARegex("[\D]+")
        assert not nfa.compute("1234100123410412346899")
        self.print_groups(nfa)

        nfa = NFARegex("[\w]+")
        assert nfa.compute("fweas_fwfwq12123e45ZKHJLKHI")
        self.print_groups(nfa)

        nfa = NFARegex("[\W]+")
        assert nfa.compute("@#$%^&*()")
        self.print_groups(nfa)

        nfa = NFARegex("[^\w\d]+")
        assert nfa.compute("@#$%^&*()")
        self.print_groups(nfa)

        nfa = NFARegex("\d+")
        assert nfa.compute("1123123asd123")
        self.print_groups(nfa)

        nfa = NFARegex("\S+")
        assert nfa.compute("1123123asd123")
        self.print_groups(nfa)

        nfa = NFARegex(".+")
        assert nfa.compute("1123123asd\n123")
        self.print_groups(nfa)

        nfa = NFARegex("[abcde0-5-]+")
        assert nfa.compute("ad23-210eszop9")
        self.print_groups(nfa)

        nfa = NFARegex("[.]+")
        assert not nfa.compute("aasd")
        assert nfa.compute("....")
        self.print_groups(nfa)

    def test24(self):
        nfa = NFARegex("^ab$")
        assert nfa.compute("ab")
        print(f'input: ab')
        self.print_groups(nfa)
        assert not nfa.compute("abb")

        nfa = NFARegex("^a$\n^b$", m=True)
        assert nfa.compute("a\nb")
        print(f'input: a\nb')
        self.print_groups(nfa)
        assert not nfa.compute("ab")

        nfa = NFARegex("a(b(c)(d))(e)", m=True)
        assert nfa.compute("abcde")
        print(f'input: abcde')
        self.print_groups(nfa)

    def test26(self):
        nfa = NFARegex("[0-8]+")
        s = "asd0123456789asdfa123adzz-.1230989ads"
        while nfa.find(s):
            self.print_groups(nfa)

        print("find all")
        ret = nfa.find_all(s)
        for r in ret:
            for k, v in r.items():
                print(v)
                print()

    def test27(self):
        nfa = NFARegex("a(?>bc|b)c")
        s = "abcc"
        assert nfa.compute(s)
        while nfa.find(s):
            self.print_groups(nfa)

        nfa.reset()
        s = "abc"
        assert not nfa.compute(s)
        print('--')
        nfa = NFARegex("a*")
        s = "aa"
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        print('--')
        nfa.reset()
        ret = nfa.find_all(s)
        for r in ret:
            for k, v in r.items():
                print(v)
                print()

    def test28(self):
        nfa = NFARegex("(a)\\1")
        s = "aa"
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        nfa = NFARegex("(['\"])[a-zA-Z]+\\1")
        s = '"easdfaeialskdjflajkei"'
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)
        nfa.reset()
        s = '"easdfeasg\''
        assert not nfa.find(s)
        nfa.reset()
        s = '\'aefasdf"'
        assert not nfa.find(s)
        nfa.reset()
        s = '\'ewwwww\''
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        nfa = NFARegex("(b)?\\1a")
        s = "a"
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        nfa = NFARegex("\\1(a)")
        s = "a"
        assert not nfa.find(s)

        nfa = NFARegex("(a\\1)")
        s = "a"
        assert not nfa.find(s)

        nfa = NFARegex("^(\\1b|a)+$")
        s = "aabb"
        assert not nfa.find(s)

        nfa = NFARegex("^(\\1b|a)+$")
        s = "aababb"
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

    def test29(self):
        print("---")
        regex = "a{2,5}"
        nfa = NFARegex(regex)
        s = "aa"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)
        print("---")
        nfa.reset()
        s = "aaa"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)
        print("---")
        nfa.reset()
        s = "aaaa"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)
        print("---")
        nfa.reset()
        s = "aaaaa"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)
        print("---")
        nfa.reset()
        s = "a"
        print(f'input:{s} ; regex:{regex} ')
        assert not nfa.compute(s)
        print("---")
        nfa.reset()
        s = "aaaaaa"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)
        print("---")
        regex = '\d{2,5}'
        nfa = NFARegex(regex)
        s = "1"
        print(f'input:{s} ; regex:{regex} ')
        assert not nfa.compute(s)
        print("---")
        nfa.reset()
        s = "21"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)
        print("---")
        nfa.reset()
        s = "21123"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        print('---')
        nfa.reset()
        s = "211afa2a3e234ad345634"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

    def test30(self):
        print('-----')
        regex = '\d{2,5}'
        nfa = NFARegex(regex)
        nfa.reset()
        s = "123412341adsf123412afd1324asdf1324as1234123454zd234"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        print('-----')
        regex = '[0-9]{2,5}?'
        nfa = NFARegex(regex)
        nfa.reset()
        s = "123412341adsf123412afd1324asdf1324as1234123454zd234"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.compute(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        # TODO this is not right
        """
        input:ccaaaaccc ; regex:(a{1,2}|c{2,3}){1,2} 
        output:
        Group 0: ccaa. Pos: [0-4] 
        Group 1: cc. Pos: [7-9] 
        Group 0: aaccc. Pos: [4-9] 
        Group 1: ccc. Pos: [6-9]
        
        expect:
        Group 0: ccaa. Pos: [0-4] 
        Group 1: aa. Pos: [2-4]       ← Here, why?  #TODO fix this ;(
        Group 0: aaccc. Pos: [4-9] 
        Group 1: ccc. Pos: [6-9]
        """
        print('-----')
        regex = '(a{1,2}|c{2,3}){1,2}'
        nfa = NFARegex(regex)
        nfa.reset()
        s = "ccaaaaccc"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        print('-----')
        regex = '(a{2,4}|c{1,2}){2}'
        nfa = NFARegex(regex)
        nfa.reset()
        s = "ccaaaaccc"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        # this is right
        print('-----')
        regex = '(?:a{2,3}|c){1}'
        nfa = NFARegex(regex)
        nfa.reset()
        s = "ccaaaaccc"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        # this is right
        print('-----')
        regex = '(?:a{2,3}|c{1,2}){1}'
        nfa = NFARegex(regex)
        nfa.reset()
        s = "ccaaaaccc"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        """
        expect:
        group 0: ccaaa. Pos: [0-5]
        group 0: ccc. Pos: [6-9]
        """
        print('-----')
        regex = '(?:a{2,3}|c{1,2}){1,2}'
        nfa = NFARegex(regex)
        nfa.reset()
        s = "ccaaaaccc"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        print('-----')
        regex = '(?:a{2,3}|c{1,2}){1,2}?'
        nfa = NFARegex(regex)
        nfa.reset()
        s = "ccaaaaccc"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        #
        print('-----')
        # regex = 'c{1,2}'
        # nfa = NFARegex(regex)
        # nfa.draw_nfa('./nfa1')
        regex = '(?:c{1,2}){1,2}'
        nfa = NFARegex(regex)
        # nfa.draw_nfa('./nfa2')
        nfa.reset()
        s = "ccccccccc"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

        print('-----')
        # regex = 'c{1,2}'
        # nfa = NFARegex(regex)
        # nfa.draw_nfa('./nfa1')
        regex = '(?:c{1,2}){1,2}?'
        nfa = NFARegex(regex)
        # nfa.draw_nfa('./nfa2')
        nfa.reset()
        s = "ccccccccc"
        print(f'input:{s} ; regex:{regex} ')
        assert nfa.find(s)
        nfa.reset()
        while nfa.find(s):
            self.print_groups(nfa)

