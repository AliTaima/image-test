import time
import logging
import subprocess


def execute(cmd):
    """
    Simple wrapper for executing command line
    """
    try:
        return subprocess.check_output(cmd, shell=True).strip().decode("utf-8")
    except Exception as e:
        return None


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    num_startup_failures = 0

    while True:

        # If it exited immediately, then we assume something happened
        # on startup (Bad credentials, deleted device, etc) and so wait
        # longer inbetween.
        if num_startup_failures > 5:
            time.sleep(60)

        start_agent_time = time.time()
        execute("service freedomrobotics start")
        logger.info("freedomrobotics service started")

        while True:

            time.sleep(10)

            result = execute("service freedomrobotics status")

            if result is None or "is running" not in result:
                logger.error("freedomrobotics service exited")

                if time.time() - start_agent_time < 30:
                    num_startup_failures += 1
                else:
                    num_startup_failures = 0
                break
