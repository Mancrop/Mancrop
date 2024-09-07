import subprocess
import locale
import utils


local_decoding = locale.getpreferredencoding()
installing_shell = "\
    pip install --upgrade uv &&\
    playwright install\
"

t = subprocess.Popen(installing_shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("Starting install requirements, maybe take a lot of time...")

while True:
    out = t.stdout.readline().decode(local_decoding)
    print(out, end='', flush=True)
    res = t.poll()
    if res is not None:
        if res == 0:
            utils.print_color(f"Successfully install requirements: exited with {res}", "green")
        else:
            utils.print_color(f"Failed(return with {res}): {t.stderr.read().decode(local_decoding)}!", "red")
        break
