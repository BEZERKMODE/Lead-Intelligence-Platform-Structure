import subprocess

def run():
    r = subprocess.run(['git', 'status'], capture_output=True, text=True)
    print("--- GIT STATUS ---")
    print("STDOUT:", r.stdout)
    print("STDERR:", r.stderr)

    r_log = subprocess.run(['git', 'log', '-n', '5', '--oneline'], capture_output=True, text=True)
    print("\n--- GIT LOG ---")
    print("STDOUT:", r_log.stdout)
    print("STDERR:", r_log.stderr)

if __name__ == '__main__':
    run()
