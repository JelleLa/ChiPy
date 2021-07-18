import chipy as cp
env = cp.environment()
cashier = cp.PriorResource(env = env, capacity = 1)
def checkout(env, ID) -> None:
    print(f"Customer {ID} arrives at the checkout at time {env.now}")
    with cashier.request() as request:     
        yield request
        yield env.timeout(5)
    print(f"Customer {ID} checked out at time {env.now}")
def run_checkout(env) -> None:
    for ID in [1,2,3,4]:
        yield env.process(checkout(env, ID))
def main():
    env.run(env.process(run_checkout(env)))
if __name__ == "__main__":
    main()
