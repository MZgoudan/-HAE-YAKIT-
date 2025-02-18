import yaml
import json
import argparse
from io import TextIOWrapper
import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox, Text
#####蜜汁狗蛋yyds##########

# YAML 转 JSON 的核心逻辑
def yaml_to_json(fileio: TextIOWrapper, save_path: str) -> str:
    all_dict_list = []
    result = yaml.load(fileio.read(), Loader=yaml.FullLoader)
    index = 0

    for group in result.get('rules', []):
        rule_group = group.get('group')
        for rule in group.get('rule', []):
            index += 1
            name = rule.get('name')
            regex = rule.get('f_regex') or rule.get('s_regex') or rule.get('regex', "")
            loaded = rule.get('loaded', False)
            scope = rule.get('scope', "")
            color = rule.get('color', "")

            yakit_dict = convert_hae_to_yakit(rule_group, name, regex, loaded, scope, color, index)
            if yakit_dict:
                all_dict_list.append(yakit_dict)

    yakit_json = json.dumps(all_dict_list, indent=4, sort_keys=True)
    if save_path:
        with open(save_path, "w", encoding="utf-8") as save_file:
            save_file.write(yakit_json)
    return yakit_json
#####蜜汁狗蛋yyds##########
#####蜜汁狗蛋yyds##########
# 将 HAE 规则转换为 YAKIT 规则
def convert_hae_to_yakit(rule_group: str, name: str, rule: str, loaded: bool, scope: str, color: str, index: int) -> dict:
    if not loaded:
        return {}
#####蜜汁狗蛋yyds##########
    yakit_dict = {
        "ExtraTag": [f"{rule_group}/{name}"],
        "VerboseName": name,
        "Rule": rule,
        "NoReplace": True,
        "Color": color,
        "Index": index,
        "EnableForRequest": True,
        "EnableForResponse": True,
        "EnableForHeader": True,
        "EnableForBody": True
    }
#####蜜汁狗蛋yyds##########
    if scope.endswith("body"):
        yakit_dict["EnableForBody"] = True
    elif scope.endswith("header"):
        yakit_dict["EnableForHeader"] = True
#####蜜汁狗蛋yyds##########
    if scope.startswith("request"):
        yakit_dict["EnableForRequest"] = True
    elif scope.startswith("response"):
        yakit_dict["EnableForResponse"] = True

    return yakit_dict
#####蜜汁狗蛋yyds##########

# GUI 主窗口
class Root(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("蜜汁狗蛋的hae转换器")
        self.style = ttk.Style()
        self.style.theme_use("xpnative")
        self.hae_yaml_file_name = None

        self.create_menu()
        self.create_yaml_text_area().grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        self.create_function_area().grid(row=0, column=2, padx=15, pady=15, sticky="nsew")
        self.create_json_text_area().grid(row=0, column=3, padx=15, pady=15, sticky="nsew")

        # 配置列权重，使布局自适应窗口大小
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
#####蜜汁狗蛋-yyds##########
    def create_menu(self):
        top_menu = Menu(self.master)
        file_menu = Menu(top_menu, tearoff=0)
        top_menu.add_cascade(label="菜单", menu=file_menu)
        file_menu.add_command(label="作者", command=self.show_author_info)
        file_menu.add_command(label="介绍", command=self.show_intro_info)
        self.master.config(menu=top_menu)

    def create_yaml_text_area(self):
        yaml_text_area = Text(width=30, height=40)
        return yaml_text_area

    def create_json_text_area(self):
        json_text_area = Text(width=30, height=40)
        return json_text_area

    def create_function_area(self):
        func_area_frame = ttk.Frame(self.master)
        ttk.Button(func_area_frame, text="打开hae规则文件", command=self.load_hae_rule_file).grid(row=0, column=0, pady=5)
        ttk.Button(func_area_frame, text="转换为yakit配置格式", command=self.convert_yaml_to_json).grid(row=1, column=0, pady=5)
        ttk.Button(func_area_frame, text="保存配置文件", command=self.save_yakit_json).grid(row=2, column=0, pady=5)
        return func_area_frame

    def load_hae_rule_file(self):
        try:
            self.hae_yaml_file_name = filedialog.askopenfilename(
                filetypes=[("hae规则文件", ".yml"), ("hae规则文件", ".yaml")],
                title="请选择hae配置文件"
            )
            if not self.hae_yaml_file_name:
                return
            with open(self.hae_yaml_file_name, encoding="utf-8") as yaml_file:
                content = yaml_file.read()
                self.master.children["!text"].delete("1.0", tk.END)
                self.master.children["!text"].insert("1.0", content)
        except Exception as e:
            messagebox.showerror("错误", f"加载文件失败：{e}")

    def convert_yaml_to_json(self):
        if not self.hae_yaml_file_name:
            messagebox.showwarning("警告", "请先选择一个hae规则文件！")
            return
        try:
            with open(self.hae_yaml_file_name, encoding="utf-8") as yaml_file:
                yakit_json = yaml_to_json(yaml_file, None)
                self.master.children["!text2"].delete("1.0", tk.END)
                self.master.children["!text2"].insert("1.0", yakit_json)
        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{e}")

    def save_yakit_json(self):
        try:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json")],
                title="保存配置文件"
            )
            if not save_path:
                return
            with open(save_path, "w", encoding="utf-8") as save_file:
                save_file.write(self.master.children["!text2"].get("1.0", tk.END))
            messagebox.showinfo("成功", f"文件已保存到 {save_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{e}")

    def show_author_info(self):
        text = "作者：蜜汁狗蛋"
        messagebox.showinfo("作者信息", text)

    def show_intro_info(self):
        text = "蜜汁狗蛋的hae转换器，一个能够将hae插件规则转换为yakit规则配置的脚本"
        messagebox.showinfo("程序介绍", text)


# 主程序入口
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="蜜汁狗蛋的hae转换器，将hae插件规则转换为yakit规则配置")
    parser.add_argument("-f", "--file", metavar="hae_rules.yaml", help="指定hae的配置文件", type=argparse.FileType(encoding="utf-8"))
    parser.add_argument("-o", "--output", metavar="savePath", help="保存指定目录", type=str, default=None)
    parser.add_argument("--gui", help="开启GUI界面", action="store_true")
    args = parser.parse_args()

    try:
        if args.gui or (not args.file and not args.output):
            root = tk.Tk()
            app = Root(master=root)
            app.grid(sticky="nsew")  # 使用 grid 布局
            root.grid_rowconfigure(0, weight=1)
            root.grid_columnconfigure(0, weight=1)
            root.mainloop()
        else:
            print(yaml_to_json(args.file, args.output))
    except Exception as e:
        print(f"程序运行时出错：{e}")