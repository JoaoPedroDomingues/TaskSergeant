import json
import os
import tkinter as tk
from copy import deepcopy
from datetime import datetime
from tkinter import messagebox, ttk

from src.Models.Assertions.assertionRetriever import AssertionRetriever
from src.Models.Tasks.superProxy import SuperProxy
from src.Utility.printer import Printer


all_categories = []
tasks = []
rules = []
output_raw = {"name": "", "version": "", "timeout": 60, "pipeline": [], "categories": []}
Printer(False, False)

def list_categories():
    deduped = []
    for category, _ in all_categories:
        if category not in deduped:
            deduped.append(category)
    return deduped


def tasks_for_category(category):
    result = []
    for cat, task_name in all_categories:
        if cat == category:
            result.append(task_name)
    return result


def parse_value(value_raw, value_type):
    value = value_raw.strip()
    if value_type == "Boolean":
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        return value
    if value_type == "Integer":
        try:
            return int(value)
        except Exception:
            return value
    if value_type == "Float":
        try:
            return float(value)
        except Exception:
            return value
    return value


def add_task_to_tree(elem, cats, task):
    if len(cats) > 0:
        cat = cats[0]
        del cats[0]

        for cat_aux in elem["categories"]:
            if cat_aux["name"] == cat:
                add_task_to_tree(cat_aux, cats, task)
                return

    task_copy = deepcopy(task)
    task_copy.pop("category", None)
    elem["tasks"].append(task_copy)


def add_category_to_tree(elem, cats):
    if len(cats) == 0:
        return

    cat = cats[0]
    del cats[0]

    for elem_aux in elem["categories"]:
        if elem_aux["name"] == cat:
            add_category_to_tree(elem_aux, cats)
            return

    next_elem = {"name": cat, "categories": [], "tasks": []}
    add_category_to_tree(next_elem, cats)
    elem["categories"].append(next_elem)


def generate_file(file_name, include_timestamp=True):
    output = output_raw
    if include_timestamp:
        output["version"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    output["pipeline"] = []
    output["categories"] = []

    for category in list_categories():
        add_category_to_tree(output, category.split("/"))

    for task in tasks:
        add_task_to_tree(output, task["category"].split("/"), task)

    output["pipeline"] = deepcopy(rules)

    os.makedirs("Inputs", exist_ok=True)
    with open(f"Inputs/{file_name}.json", "w", encoding="utf-8") as file_handle:
        file_handle.write(json.dumps(output, indent=2))

    output_raw["pipeline"] = []
    output_raw["categories"] = []


class ValueEditor(tk.Toplevel):
    def __init__(self, parent, title, initial=None, keyed=False):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.result = None
        self.keyed = keyed

        self.value_kind = tk.StringVar(value="None")
        self.type_var = tk.StringVar(value="String")
        self.key_var = tk.StringVar()
        self.value_var = tk.StringVar()
        self.items = []

        self._build_ui()
        if initial is not None:
            self._load_initial(initial)
        self._refresh_items()

        self.transient(parent)
        self.grab_set()
        self.wait_visibility()
        self.focus_set()

    def _build_ui(self):
        container = ttk.Frame(self, padding=10)
        container.grid(row=0, column=0, sticky="nsew")

        ttk.Label(container, text="Value shape").grid(row=0, column=0, sticky="w")
        ttk.Combobox(
            container,
            textvariable=self.value_kind,
            state="readonly",
            values=("None", "Single", "List", "Composed"),
            width=12,
        ).grid(row=0, column=1, sticky="w", padx=(8, 0))

        self.value_kind.trace_add("write", lambda *_: self._refresh_items())

        entry_row = ttk.Frame(container)
        entry_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        if self.keyed:
            ttk.Label(entry_row, text="Key").grid(row=0, column=0, sticky="w")
            ttk.Entry(entry_row, textvariable=self.key_var, width=16).grid(
                row=0, column=1, sticky="w", padx=(6, 8)
            )

        ttk.Label(entry_row, text="Value").grid(row=0, column=2, sticky="w")
        ttk.Entry(entry_row, textvariable=self.value_var, width=18).grid(
            row=0, column=3, sticky="w", padx=(6, 8)
        )
        ttk.Combobox(
            entry_row,
            textvariable=self.type_var,
            state="readonly",
            values=("String", "Boolean", "Integer", "Float"),
            width=10,
        ).grid(row=0, column=4, sticky="w")
        ttk.Button(entry_row, text="Add", command=self._add_item).grid(
            row=0, column=5, sticky="w", padx=(8, 0)
        )

        self.items_list = tk.Listbox(container, width=70, height=7)
        self.items_list.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        controls = ttk.Frame(container)
        controls.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Button(controls, text="Remove Selected", command=self._remove_selected).pack(
            side="left"
        )
        ttk.Button(controls, text="Cancel", command=self.destroy).pack(side="right")
        ttk.Button(controls, text="Apply", command=self._apply).pack(side="right", padx=(0, 8))

    def _load_initial(self, initial):
        if initial is None:
            return
        if isinstance(initial, list):
            self.value_kind.set("List")
            for value in initial:
                self.items.append(("", value))
        elif isinstance(initial, dict):
            self.value_kind.set("Composed")
            for key, value in initial.items():
                self.items.append((str(key), value))
        else:
            self.value_kind.set("Single")
            self.items = [("", initial)]

    def _refresh_items(self):
        kind = self.value_kind.get()
        if kind in ("None", "Single"):
            self.items_list.configure(height=1)
        else:
            self.items_list.configure(height=7)
        self._render_items()

    def _render_items(self):
        self.items_list.delete(0, tk.END)
        for key, value in self.items:
            if key:
                self.items_list.insert(tk.END, f"{key}: {repr(value)}")
            else:
                self.items_list.insert(tk.END, repr(value))

    def _add_item(self):
        kind = self.value_kind.get()
        if kind == "None":
            messagebox.showinfo("Value", "Set shape to Single, List, or Composed first.")
            return

        key = self.key_var.get().strip()
        if kind == "Composed" and self.keyed and not key:
            messagebox.showwarning("Value", "Composed values require a key.")
            return

        parsed = parse_value(self.value_var.get(), self.type_var.get())

        if kind == "Single":
            self.items = [("", parsed)]
        elif kind == "List":
            self.items.append(("", parsed))
        else:
            for index, (existing_key, _) in enumerate(self.items):
                if existing_key == key:
                    self.items[index] = (key, parsed)
                    self._render_items()
                    return
            self.items.append((key, parsed))

        self._render_items()

    def _remove_selected(self):
        selected = self.items_list.curselection()
        if not selected:
            return
        del self.items[selected[0]]
        self._render_items()

    def _apply(self):
        kind = self.value_kind.get()
        if kind == "None":
            self.result = None
        elif kind == "Single":
            if not self.items:
                messagebox.showwarning("Value", "Add a value first.")
                return
            self.result = self.items[0][1]
        elif kind == "List":
            self.result = [item[1] for item in self.items]
        else:
            composed = {}
            for key, value in self.items:
                if not key:
                    messagebox.showwarning("Value", "Every composed entry needs a key.")
                    return
                composed[key] = value
            self.result = composed

        self.destroy()


class RuleValueDialog(tk.Toplevel):
    def __init__(self, parent, initial=None):
        super().__init__(parent)
        self.title("Rule Key")
        self.resizable(False, False)
        self.result = None

        self.value_var = tk.StringVar(value="" if initial is None else str(initial))
        self.type_var = tk.StringVar(value="String")

        frame = ttk.Frame(self, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Key Value").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.value_var, width=24).grid(
            row=0, column=1, sticky="w", padx=(6, 8)
        )
        ttk.Combobox(
            frame,
            textvariable=self.type_var,
            state="readonly",
            values=("String", "Boolean", "Integer", "Float"),
            width=10,
        ).grid(row=0, column=2, sticky="w")

        controls = ttk.Frame(frame)
        controls.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        ttk.Button(controls, text="Cancel", command=self.destroy).pack(side="right")
        ttk.Button(controls, text="Apply", command=self._apply).pack(side="right", padx=(0, 8))

        self.transient(parent)
        self.grab_set()
        self.wait_visibility()
        self.focus_set()

    def _apply(self):
        self.result = parse_value(self.value_var.get(), self.type_var.get())
        self.destroy()


class TaskBuilderGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TaskSergeant Task Builder")
        self.geometry("1150x740")

        self.all_assertions = list(AssertionRetriever.genDict())
        self._load_categories()

        self.task_value = None
        self.expected_value = None
        self.rule_key = None

        self._build_ui()
        self._refresh_tasks_list()
        self._refresh_rules_list()
        self._refresh_rule_selectors()

    def _load_categories(self):
        def add_categories(category, name):
            for sub_category in category:
                if sub_category == "tasks":
                    for task_name in category[sub_category]:
                        all_categories.append((name, task_name))
                else:
                    add_categories(category[sub_category], sub_category)

        proxy_information = SuperProxy.genDict()
        for category in proxy_information:
            add_categories(proxy_information[category], category)

    def _build_ui(self):
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=2)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        metadata = ttk.LabelFrame(root, text="Input File Metadata", padding=10)
        metadata.grid(row=0, column=0, columnspan=2, sticky="ew")
        metadata.columnconfigure(1, weight=1)
        metadata.columnconfigure(3, weight=1)

        self.name_var = tk.StringVar(value=output_raw["name"])
        self.timeout_var = tk.StringVar(value=str(output_raw["timeout"]))

        ttk.Label(metadata, text="Name").grid(row=0, column=0, sticky="w")
        ttk.Entry(metadata, textvariable=self.name_var).grid(
            row=0, column=1, sticky="ew", padx=(6, 12)
        )
        ttk.Label(metadata, text="Timeout (seconds)").grid(row=0, column=2, sticky="w")
        ttk.Entry(metadata, textvariable=self.timeout_var, width=14).grid(
            row=0, column=3, sticky="w", padx=(6, 0)
        )

        self.name_var.trace_add("write", lambda *_: self._update_metadata())
        self.timeout_var.trace_add("write", lambda *_: self._update_metadata())

        left = ttk.LabelFrame(root, text="Tasks", padding=10)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(10, 0))
        left.columnconfigure(1, weight=1)
        left.rowconfigure(8, weight=1)

        self.category_var = tk.StringVar()
        self.task_name_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.repeatable_var = tk.StringVar(value="1")
        self.assertion_var = tk.StringVar(value="")

        ttk.Label(left, text="Category").grid(row=0, column=0, sticky="w")
        self.category_box = ttk.Combobox(
            left, textvariable=self.category_var, values=list_categories(), state="readonly"
        )
        self.category_box.grid(row=0, column=1, sticky="ew", padx=(6, 0))
        self.category_var.trace_add("write", lambda *_: self._on_category_changed())

        ttk.Label(left, text="Task").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.task_box = ttk.Combobox(left, textvariable=self.task_name_var, state="readonly")
        self.task_box.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(8, 0))

        ttk.Label(left, text="Description").grid(row=2, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(left, textvariable=self.description_var).grid(
            row=2, column=1, sticky="ew", padx=(6, 0), pady=(8, 0)
        )

        ttk.Label(left, text="Repeatable").grid(row=3, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(left, textvariable=self.repeatable_var, width=8).grid(
            row=3, column=1, sticky="w", padx=(6, 0), pady=(8, 0)
        )

        task_value_row = ttk.Frame(left)
        task_value_row.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Button(task_value_row, text="Task Parameter", command=self._edit_task_value).pack(
            side="left"
        )
        self.task_value_label = ttk.Label(task_value_row, text="None")
        self.task_value_label.pack(side="left", padx=(8, 0))

        ttk.Label(left, text="Assertion").grid(row=5, column=0, sticky="w", pady=(8, 0))
        ttk.Combobox(
            left,
            textvariable=self.assertion_var,
            values=[""] + self.all_assertions,
            state="readonly",
        ).grid(row=5, column=1, sticky="ew", padx=(6, 0), pady=(8, 0))

        expected_row = ttk.Frame(left)
        expected_row.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Button(expected_row, text="Expected Value", command=self._edit_expected_value).pack(
            side="left"
        )
        self.expected_label = ttk.Label(expected_row, text="None")
        self.expected_label.pack(side="left", padx=(8, 0))

        actions = ttk.Frame(left)
        actions.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Button(actions, text="Add Task", command=self._add_task).pack(side="left")
        ttk.Button(actions, text="Delete Selected Task", command=self._delete_selected_task).pack(
            side="left", padx=(8, 0)
        )

        self.tasks_list = tk.Listbox(left, height=12)
        self.tasks_list.grid(row=8, column=0, columnspan=2, sticky="nsew", pady=(8, 0))

        save_frame = ttk.Frame(left)
        save_frame.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        self.file_name_var = tk.StringVar(value="autosaved")
        ttk.Label(save_frame, text="Save As").pack(side="left")
        ttk.Entry(save_frame, textvariable=self.file_name_var, width=20).pack(
            side="left", padx=(6, 8)
        )
        ttk.Button(save_frame, text="Save Input File", command=self._save_manual).pack(side="left")

        right = ttk.LabelFrame(root, text="Hierarchy Rules", padding=10)
        right.grid(row=1, column=1, sticky="nsew", pady=(10, 0))
        right.columnconfigure(1, weight=1)
        right.rowconfigure(5, weight=1)

        self.parent_var = tk.StringVar()
        self.child_var = tk.StringVar()
        self.use_rule_key_var = tk.BooleanVar(value=False)

        ttk.Label(right, text="Parent Task").grid(row=0, column=0, sticky="w")
        self.parent_box = ttk.Combobox(right, textvariable=self.parent_var, state="readonly")
        self.parent_box.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ttk.Label(right, text="Child Task").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.child_box = ttk.Combobox(right, textvariable=self.child_var, state="readonly")
        self.child_box.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=(8, 0))

        key_row = ttk.Frame(right)
        key_row.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        ttk.Checkbutton(
            key_row,
            text="Add Rule Key",
            variable=self.use_rule_key_var,
            command=self._toggle_rule_key,
        ).pack(side="left")
        self.rule_key_button = ttk.Button(key_row, text="Edit Key", command=self._edit_rule_key)
        self.rule_key_button.pack(side="left", padx=(8, 0))
        self.rule_key_label = ttk.Label(key_row, text="None")
        self.rule_key_label.pack(side="left", padx=(8, 0))
        self.rule_key_button.state(["disabled"])

        ttk.Button(right, text="Add Rule", command=self._add_rule).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(8, 0)
        )
        ttk.Button(right, text="Delete Selected Rule", command=self._delete_rule).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(8, 0)
        )

        self.rules_list = tk.Listbox(right)
        self.rules_list.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(8, 0))

        if self.category_box["values"]:
            self.category_var.set(self.category_box["values"][0])

    def _update_metadata(self):
        output_raw["name"] = self.name_var.get()
        try:
            output_raw["timeout"] = float(self.timeout_var.get())
        except Exception:
            pass
        self._autosave()

    def _on_category_changed(self):
        options = tasks_for_category(self.category_var.get())
        self.task_box["values"] = options
        if options:
            self.task_name_var.set(options[0])
        else:
            self.task_name_var.set("")

    def _edit_task_value(self):
        dialog = ValueEditor(self, "Task Parameter", initial=self.task_value, keyed=True)
        self.wait_window(dialog)
        self.task_value = dialog.result
        self.task_value_label.configure(text=self._short_value(self.task_value))

    def _edit_expected_value(self):
        dialog = ValueEditor(self, "Expected Value", initial=self.expected_value, keyed=True)
        self.wait_window(dialog)
        self.expected_value = dialog.result
        self.expected_label.configure(text=self._short_value(self.expected_value))

    def _toggle_rule_key(self):
        if self.use_rule_key_var.get():
            self.rule_key_button.state(["!disabled"])
        else:
            self.rule_key_button.state(["disabled"])
            self.rule_key = None
            self.rule_key_label.configure(text="None")

    def _edit_rule_key(self):
        dialog = RuleValueDialog(self, initial=self.rule_key)
        self.wait_window(dialog)
        self.rule_key = dialog.result
        self.rule_key_label.configure(text=self._short_value(self.rule_key))

    def _short_value(self, value):
        if value is None:
            return "None"
        text = repr(value)
        return text if len(text) < 42 else text[:39] + "..."

    def _add_task(self):
        category = self.category_var.get().strip()
        task_name = self.task_name_var.get().strip()
        description = self.description_var.get().strip()

        if not category or not task_name:
            messagebox.showwarning("Task", "Category and task are required.")
            return
        if not description:
            messagebox.showwarning("Task", "Description is required.")
            return

        try:
            repeatable = int(self.repeatable_var.get())
        except Exception:
            repeatable = 1

        new_task = {
            "category": category,
            "task": task_name,
            "description": description,
            "repeatable": repeatable,
            "id": "task_{:03d}".format(len(tasks) + 1),
        }

        if self.task_value is not None:
            new_task["value"] = self.task_value

        assertion = self.assertion_var.get().strip()
        if assertion:
            new_task["assertionType"] = assertion
            if self.expected_value is not None:
                new_task["expected"] = self.expected_value

        tasks.append(new_task)
        self._refresh_tasks_list()
        self._refresh_rule_selectors()
        self._autosave()

    def _delete_selected_task(self):
        selected = self.tasks_list.curselection()
        if not selected:
            return

        task = tasks[selected[0]]
        del tasks[selected[0]]

        task_id = task.get("id")
        if task_id:
            rules[:] = [
                rule
                for rule in rules
                if rule.get("id") != task_id
                and rule.get("paths", [{}])[0].get("nextSlotId") != task_id
            ]

        self._refresh_tasks_list()
        self._refresh_rules_list()
        self._refresh_rule_selectors()
        self._autosave()

    def _refresh_tasks_list(self):
        self.tasks_list.delete(0, tk.END)
        for index, task in enumerate(tasks):
            self.tasks_list.insert(
                index, f"{index} - {task.get('id', 'None')}: {task['description']}"
            )

    def _refresh_rule_selectors(self):
        ids = [task["id"] for task in tasks if task.get("id")]
        self.parent_box["values"] = ids
        self.child_box["values"] = ids
        if ids:
            if self.parent_var.get() not in ids:
                self.parent_var.set(ids[0])
            if self.child_var.get() not in ids:
                self.child_var.set(ids[0])
        else:
            self.parent_var.set("")
            self.child_var.set("")

    def _add_rule(self):
        parent = self.parent_var.get().strip()
        child = self.child_var.get().strip()
        if not parent or not child:
            messagebox.showwarning("Rule", "Parent and child tasks are required.")
            return

        if self.use_rule_key_var.get() and self.rule_key is not None:
            rules.append({"id": parent, "paths": [{"key": self.rule_key, "nextSlotId": child}]})
        else:
            rules.append({"id": parent, "paths": [{"nextSlotId": child}]})

        self._refresh_rules_list()
        self._autosave()

    def _delete_rule(self):
        selected = self.rules_list.curselection()
        if not selected:
            return
        del rules[selected[0]]
        self._refresh_rules_list()
        self._autosave()

    def _refresh_rules_list(self):
        self.rules_list.delete(0, tk.END)
        for index, rule in enumerate(rules):
            parent = rule["id"]
            path = rule["paths"][0]
            child = path["nextSlotId"]
            key = path.get("key", "{Any value}")
            self.rules_list.insert(index, f"{index} - {parent}->{child} : {key}")

    def _save_manual(self):
        file_name = self.file_name_var.get().strip()
        if not file_name:
            messagebox.showwarning("Save", "File name cannot be empty.")
            return
        generate_file(file_name)
        messagebox.showinfo("Save", f"Saved Inputs/{file_name}.json")

    def _autosave(self):
        try:
            generate_file("autosaved")
        except Exception:
            pass


if __name__ == "__main__":
    app = TaskBuilderGUI()
    app.mainloop()
