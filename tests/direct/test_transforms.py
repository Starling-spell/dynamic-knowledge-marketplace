import hashlib
import json


A = "At collection, label each water sample with site, date, collector, and sample ID before transport."
B = "At laboratory receipt, log the sample ID, receipt time, and condition. Quarantine a sample with no ID."
GOOD = ("Attach a label with site, date, collector, and sample ID before transport. "
        "At the laboratory, log the ID, receipt time, and condition. Quarantine missing-ID samples.")
BAD = "The laboratory may analyze samples without an ID and skip receipt logging."


def sha(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def setup(direct_vm, direct_deploy, direct_alice, output=GOOD, expected_output=None):
    direct_vm.sender = direct_alice
    contract = direct_deploy("contracts/DynamicKnowledgeMarketplace.py")
    contract.create_space("samples", "Water sampling instructions")
    contract.publish_source("samples", "field", "GUIDE", "https://a.example/field", sha(A))
    contract.publish_source("samples", "lab", "GUIDE", "https://b.example/lab", sha(B))
    direct_vm.mock_web(r".*a\.example/field", {"status": 200, "body": A})
    direct_vm.mock_web(r".*b\.example/lab", {"status": 200, "body": B})
    direct_vm.mock_web(r".*out\.example/merged", {"status": 200, "body": output})
    contract.propose_transform("samples", "merge-1", "MERGE", "field", "lab",
                               "combined", "https://out.example/merged",
                               expected_output or sha(output), "GUIDE", "")
    return contract


def verdict(direct_vm, coverage="PASS", grounding="PASS", meaning="PASS", category="PASS"):
    direct_vm.mock_llm(r".*Evaluate the transformation of the actual full source text.*",
                       json.dumps({"coverage": coverage, "grounding": grounding,
                                   "meaning_preserved": meaning, "category_fit": category}))


def test_merged_output_becomes_composable_asset(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    verdict(direct_vm)
    contract.apply_transform("samples", "merge-1")
    assert contract.get_transform("samples", "merge-1")["state"] == "PUBLISHED"
    asset = contract.get_asset("samples", "combined")
    assert asset["kind"] == "TRANSFORMED"
    assert asset["input_a"] == "field" and asset["input_b"] == "lab"
    assert asset["depth"] == 1
    assert contract.get_space("samples")["derived"] == 1
    with direct_vm.expect_revert("terminal transformation"):
        contract.apply_transform("samples", "merge-1")


def test_contradictory_output_rejected_without_asset(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice, output=BAD)
    verdict(direct_vm, coverage="FAIL", grounding="FAIL", meaning="FAIL")
    contract.apply_transform("samples", "merge-1")
    assert contract.get_transform("samples", "merge-1")["state"] == "REJECTED"
    assert contract.get_space("samples")["derived"] == 0
    assert json.loads(contract.get_record("samples", "merge-1"))["packet"]["report"]["vector"] == ["FAIL", "FAIL", "FAIL", "PASS"]


def test_wrong_output_hash_fails_closed(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice, expected_output="0" * 64)
    verdict(direct_vm)
    contract.apply_transform("samples", "merge-1")
    assert contract.get_transform("samples", "merge-1")["state"] == "INCONCLUSIVE"
    record = json.loads(contract.get_record("samples", "merge-1"))
    assert record["packet"]["report"]["matches"][-1] is False


def test_unknown_semantics_cannot_publish(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    verdict(direct_vm, grounding="UNKNOWN")
    contract.apply_transform("samples", "merge-1")
    assert contract.get_transform("samples", "merge-1")["state"] == "INCONCLUSIVE"


def test_cross_space_and_duplicate_output_rejected(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    contract.create_space("other", "Another bounded collection")
    with direct_vm.expect_revert("first input must exist in this space"):
        contract.propose_transform("other", "cross", "RESTRUCTURE", "field", "",
                                   "out", "https://out.example/merged", sha(GOOD), "GUIDE", "")
    verdict(direct_vm)
    contract.apply_transform("samples", "merge-1")
    with direct_vm.expect_revert("unique transformation and output required"):
        contract.propose_transform("samples", "again", "EXTRACT", "combined", "",
                                   "combined", "https://out.example/extract", sha(GOOD),
                                   "GUIDE", "ID")


def test_invalid_source_url_and_hash(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    contract = direct_deploy("contracts/DynamicKnowledgeMarketplace.py")
    contract.create_space("samples", "Water sampling instructions")
    with direct_vm.expect_revert("bounded category, HTTPS URL and SHA-256"):
        contract.publish_source("samples", "private", "GUIDE", "https://127.0.0.1/private", sha(A))
    with direct_vm.expect_revert("bounded category, HTTPS URL and SHA-256"):
        contract.publish_source("samples", "fake", "GUIDE", "https://a.example/field", "abcd")


def test_merge_needs_two_distinct_inputs(direct_vm, direct_deploy, direct_alice):
    contract = setup(direct_vm, direct_deploy, direct_alice)
    with direct_vm.expect_revert("MERGE needs two distinct inputs"):
        contract.propose_transform("samples", "bad", "MERGE", "field", "field",
                                   "new", "https://out.example/new", sha(GOOD), "GUIDE", "")
