#!/usr/bin/env python3
"""
テスト実行スクリプト
使い方: python tests/run_tests.py
"""
import subprocess
import sys
from pathlib import Path


def run_tests():
    """テストを実行"""
    project_root = Path(__file__).parent.parent

    print("🧪 Live Chat API テスト実行開始〜！")

    commands = [
        # 全テスト実行
        {
            "cmd": ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
            "desc": "📝 全テスト実行",
        },
        # カバレッジ付きテスト実行
        {
            "cmd": [
                "python",
                "-m",
                "pytest",
                "tests/",
                "--cov=app",
                "--cov-report=term-missing",
            ],
            "desc": "📊 カバレッジ付きテスト実行",
        },
    ]

    for command_info in commands:
        cmd = command_info["cmd"]
        desc = command_info["desc"]

        print(f"\n{desc}")
        print(f"🚀 実行中: {' '.join(cmd)}")

        result = subprocess.run(cmd, cwd=project_root)
        if result.returncode != 0:
            print(f"❌ コマンドが失敗したよ〜: {' '.join(cmd)}")
            return False
        else:
            print(f"✅ 成功〜！")

    print("\n🎉 全テスト完了！お疲れさま〜💖")
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
