import pytest
from similar.similar import Similar, best_match, NoResultException

@pytest.fixture
def sample_words():
    return ["apple", "raspberry", "pear", "banana"]


@pytest.fixture
def similar_instance(sample_words):
    return Similar("bananna", sample_words)


@pytest.mark.parametrize("input_word,expected", [
    ("bananna", "banana"),
    ("rasbery", "raspberry"),
    ("aple", "apple"),
])
def test_best_multiple(input_word, expected):
    s = Similar(input_word, ["apple", "raspberry", "pear", "banana"])
    assert s.best() == expected


def test_results_returns_list_of_tuples(similar_instance):
    results = similar_instance.results()
    assert isinstance(results, list)
    assert all(isinstance(item, tuple) for item in results)
    assert all(isinstance(item[0], str) for item in results)
    assert all(isinstance(item[1], float) for item in results)


def test_results_sorted_descending(similar_instance):
    results = similar_instance.results()
    scores = [score for _, score in results]
    assert scores == sorted(scores, reverse=True)


def test_best_matches_first_result(similar_instance):
    results = similar_instance.results()
    assert similar_instance.best() == results[0][0]


def test_no_result_exception_on_empty_list():
    s = Similar("test", [])
    with pytest.raises(NoResultException):
        s.best()


def test_no_result_exception_on_no_match():
    s = Similar("zzz", [])
    with pytest.raises(NoResultException):
        s.results()


def test_results_are_strictly_sorted():
    s = Similar("abc", ["abc", "abd", "zzz"])
    results = s.results()
    for i in range(len(results) - 1):
        assert results[i][1] >= results[i + 1][1]


def test_deterministic_results():
    words = ["apple", "raspberry", "pear", "banana"]
    s1 = Similar("bananna", words)
    s2 = Similar("bananna", words)
    assert s1.results() == s2.results()


def test_generator_input():
    def genwords():
        for word in ["apple", "raspberry", "pear", "banana"]:
            yield word
    s = Similar("bananna", genwords())
    assert s.best() == "banana"


def test_file_like_input(tmp_path):
    file = tmp_path / "words.txt"
    file.write_text("apple\nraspberry\npear\nbanana\n")
    with open(file) as f:
        s = Similar("bananna", f)
        assert s.best() == "banana"


def test_best_match_function():
    words = ["apple", "raspberry", "pear", "banana"]
    best = best_match("bananna", words)
    assert best == "banana"
