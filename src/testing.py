from utils import genepool, hyperparamters, ruleset, individuals_of_generation


def test_parameters(run):

    print(f"Hyperparameters: {hyperparamters(run)}\n")
    print(f"Hyperparameters type: {type(hyperparamters(run))}\n")

    print(f"Genepool: {genepool(run)}\n")
    print(f"Genepool type: {type(genepool(run))}\n")

    print(f"Ruleset: {ruleset(run)}\n")
    print(f"Ruleset type: {type(ruleset(run))}\n")


def test_individuals(run, generation, individual):

    l = individuals_of_generation(run, 1, value="results")

    for li in l:
        print("\nKEY:\n", li.keys())
        print("VALUE:\n", li.values())


def main():
    run = "ga_20230116-110958_sc_2d_4classes"
    generation = 1
    individual = "abstract_wildebeest"

    test_parameters(run)

if __name__ == "__main__":
    main()
