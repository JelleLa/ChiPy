import chipy as cp
env = cp.environment()
def machine(env, ID) -> None:
    print(f"Product {ID} enters at time {env.now}")
    if ((ID % 2) == 0):
        yield env.timeout(1)
    else:
        yield env.timeout(2)
    print(f"Product {ID} exits at time {env.now}")
def run_machine(env) -> None:
    for ID in [1,2,3,4]:
        yield env.process(machine(env, ID))
def main():
    env.run(env.process(run_machine(env)))
if __name__ == "__main__":
    main()
