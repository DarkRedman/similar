import operator
from rapidfuzz import distance, process, fuzz
from .exceptions import NoResultException


ALGOS = {
    "levenshtein": distance.Levenshtein.normalized_similarity,
    "damerau": distance.DamerauLevenshtein.normalized_similarity,
    "osa": distance.OSA.normalized_similarity,
    "jaro": distance.Jaro.normalized_similarity,
    "winkler": distance.JaroWinkler.normalized_similarity,
    "hamming": distance.Hamming.normalized_similarity,
    "indel": distance.Indel.normalized_similarity,
    "lcs": distance.LCSseq.normalized_similarity,
    "prefix": distance.Prefix.normalized_similarity,
    "suffix": distance.Postfix.normalized_similarity,
    "qratio": fuzz.QRatio,
    "wratio": fuzz.WRatio,

    # aliases
    "typo": distance.DamerauLevenshtein.normalized_similarity,
    "fast_typo": distance.OSA.normalized_similarity,
    "name": distance.JaroWinkler.normalized_similarity,
    "fuzzy": distance.JaroWinkler.normalized_similarity,
    "strict": distance.Levenshtein.normalized_similarity,
    "edit": distance.Levenshtein.normalized_similarity,
    "structure": distance.LCSseq.normalized_similarity,
    "fast": distance.Indel.normalized_similarity,
    "quick_ratio": fuzz.QRatio,
    "weighted_ratio": fuzz.QRatio,
}


class Similar(object):
    """
    The main class used to search similar words.
    """

    def __init__(
        self,
        needle,
        haystack,
        algo="levenshtein",
        score_cutoff=None,
        score_hint=None,
        processor=None,
        top_k=None
    ):
        self.needle = needle
        self.haystack = haystack
        self.processor = processor
        self.score_cutoff = score_cutoff
        self.score_hint = score_hint
        self.top_k = top_k

        if algo not in ALGOS:
            raise ValueError(f"Unknown algo: {algo}")

        self.algo = ALGOS[algo]

    def best(self):
        """
        Returns the best similar word.
        """
        results = self.results()
        return results[0][0]

    def results(self):
        """
        Returns a list of tuple, ordered by similarity.
        """
        results = process.extract(
            self.needle,
            [word.strip() for word in self.haystack],
            scorer=self.algo,
            processor=self.processor,
            score_cutoff=self.score_cutoff,
            score_hint=self.score_hint,
            limit=self.top_k,
        )

        if not results:
            raise NoResultException('No similar word found.')

        return [(choice, score) for choice, score, _ in results]


def best_match(needle, haystack):
    """
    Constructs a Similar object and returns the best result found.
    """
    p = Similar(needle, haystack)
    return p.best()
