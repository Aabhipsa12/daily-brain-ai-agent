"""
Daily Brain — Core Agent & Tool Function Test Suite (Standard Library unittest)
Author: Daily Brain Engineering Team
"""

import os
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta
import main

class TestDailyBrainCore(unittest.TestCase):

    def setUp(self):
        """Create a temporary isolated storage environment for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.test_tasks_file = os.path.join(self.test_dir, "tasks.json")
        self.original_get_storage_path = main.get_storage_path
        main.get_storage_path = lambda: self.test_tasks_file

    def tearDown(self):
        """Clean up temporary test artifacts."""
        main.get_storage_path = self.original_get_storage_path
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_task_basic(self):
        """Verify standard task creation with defaults."""
        res = main.save_task(task="Write Unit Tests", priority="medium")
        self.assertIn("saved task:", res.lower())
        
        tasks = main.get_saved_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["task"], "Write Unit Tests")
        self.assertEqual(tasks[0]["priority"], "medium")
        self.assertEqual(tasks[0]["category"], "General")
        self.assertEqual(tasks[0]["status"], "pending")

    def test_save_task_with_category_and_subtasks(self):
        """Verify task creation with custom priority, category, and checklist subtasks."""
        subtasks = ["Write setup", "Write assertions", "Run tests"]
        res = main.save_task(
            task="Finish Testing Suite",
            priority="high",
            due_date="2026-12-31",
            category="Academics",
            subtasks=subtasks
        )
        self.assertIn("saved task:", res.lower())
        self.assertIn("3 sub-steps", res.lower())
        
        tasks = main.get_saved_tasks()
        self.assertEqual(len(tasks), 1)
        t = tasks[0]
        self.assertEqual(t["priority"], "high")
        self.assertEqual(t["category"], "Academics")
        self.assertEqual(len(t["subtasks"]), 3)
        self.assertEqual(t["subtasks"][0]["title"], "Write setup")
        self.assertFalse(t["subtasks"][0]["done"])

    def test_toggle_and_complete_task(self):
        """Verify task completion and toggling logic."""
        main.save_task(task="Submit Project", priority="high")
        tasks = main.get_saved_tasks()
        self.assertEqual(tasks[0]["status"], "pending")
        
        # Toggle via index
        main.toggle_task_status(0)
        tasks = main.get_saved_tasks()
        self.assertEqual(tasks[0]["status"], "completed")
        
        # Toggle back
        main.toggle_task_status(0)
        tasks = main.get_saved_tasks()
        self.assertEqual(tasks[0]["status"], "pending")
        
        # Complete via agent tool
        res = main.complete_task("Submit Project")
        self.assertIn("as completed", res.lower())
        tasks = main.get_saved_tasks()
        self.assertEqual(tasks[0]["status"], "completed")

    def test_subtask_operations(self):
        """Verify adding, toggling, and deleting checklist subtasks."""
        main.save_task(task="Prepare Presentation", priority="medium", subtasks=["Design slides"])
        
        # Add subtask
        main.add_subtask_to_task(0, "Practice speaking")
        tasks = main.get_saved_tasks()
        self.assertEqual(len(tasks[0]["subtasks"]), 2)
        self.assertEqual(tasks[0]["subtasks"][1]["title"], "Practice speaking")
        
        # Toggle subtask
        main.toggle_subtask_status(0, 0)
        tasks = main.get_saved_tasks()
        self.assertTrue(tasks[0]["subtasks"][0]["done"])
        
        # Delete subtask
        main.delete_subtask_by_index(0, 0)
        tasks = main.get_saved_tasks()
        self.assertEqual(len(tasks[0]["subtasks"]), 1)
        self.assertEqual(tasks[0]["subtasks"][0]["title"], "Practice speaking")

    def test_delete_task(self):
        """Verify task deletion via index and agent tool name search."""
        main.save_task(task="Delete Me Later", priority="low")
        main.save_task(task="Keep Me Safe", priority="high")
        self.assertEqual(len(main.get_saved_tasks()), 2)
        
        # Agent tool delete
        res = main.delete_task("Delete Me")
        self.assertIn("deleted task", res.lower())
        tasks = main.get_saved_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["task"], "Keep Me Safe")
        
        # Index delete
        main.delete_task_by_index(0)
        self.assertEqual(len(main.get_saved_tasks()), 0)

    def test_deadline_and_urgency_calculation(self):
        """Verify deadline classification for overdue, due today, and upcoming tasks."""
        today_str = datetime.now().strftime("%Y-%m-%d")
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        t_overdue = {"task": "Old", "due_date": yesterday_str, "status": "pending"}
        t_today = {"task": "Today", "due_date": today_str, "status": "pending"}
        t_tomorrow = {"task": "Tomorrow", "due_date": tomorrow_str, "status": "pending"}
        
        code1, label1, _ = main.get_deadline_status(t_overdue)
        self.assertEqual(code1, "overdue")
        self.assertIn("overdue", label1.lower())
        
        code2, label2, _ = main.get_deadline_status(t_today)
        self.assertEqual(code2, "due_today")
        self.assertIn("due today", label2.lower())
        
        code3, label3, _ = main.get_deadline_status(t_tomorrow)
        self.assertEqual(code3, "due_tomorrow")
        self.assertIn("due tomorrow", label3.lower())

    def test_get_current_date(self):
        """Verify dynamic date resolution returns valid ISO/formatted date string."""
        date_str = main.get_current_date()
        today_year = str(datetime.now().year)
        self.assertIn(today_year, date_str)

if __name__ == "__main__":
    unittest.main()
