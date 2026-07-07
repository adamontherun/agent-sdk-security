"""Tests for Chapter 5 — acceptEdits auto-approval model."""

CWD = "/home/dev/project"
EXTRA = ["/home/dev/shared"]


def test_command_list_is_exact(subject):
    assert {
        "mkdir",
        "touch",
        "rm",
        "rmdir",
        "mv",
        "cp",
        "sed",
    } == subject.ACCEPT_EDITS_FS_COMMANDS


def test_edit_in_working_dir_approved(subject):
    assert subject.accept_edits_approves("Edit", {"file_path": "src/app.py"}, CWD, EXTRA)


def test_edit_outside_scope_prompts(subject):
    assert not subject.accept_edits_approves("Edit", {"file_path": "/etc/hosts"}, CWD, EXTRA)


def test_edit_in_additional_dir_approved(subject):
    assert subject.accept_edits_approves(
        "Write", {"file_path": "/home/dev/shared/notes.md"}, CWD, EXTRA
    )


def test_mkdir_in_scope_approved(subject):
    assert subject.accept_edits_approves("Bash", {"command": "mkdir build"}, CWD, EXTRA)


def test_rm_in_scope_approved(subject):
    assert subject.accept_edits_approves("Bash", {"command": "rm src/old.py"}, CWD, EXTRA)


def test_non_fs_command_not_approved(subject):
    assert not subject.accept_edits_approves(
        "Bash", {"command": "curl https://example.com"}, CWD, EXTRA
    )


def test_fs_command_outside_scope_prompts(subject):
    assert not subject.accept_edits_approves("Bash", {"command": "rm /etc/passwd"}, CWD, EXTRA)


def test_circuit_breaker_rm_rf_root(subject):
    assert subject.is_circuit_breaker("rm -rf /")
    assert not subject.accept_edits_approves("Bash", {"command": "rm -rf /"}, CWD, EXTRA)


def test_circuit_breaker_rm_rf_home(subject):
    assert subject.is_circuit_breaker("rm -rf ~")


def test_read_tool_not_a_file_edit(subject):
    assert not subject.accept_edits_approves("Read", {"file_path": "src/app.py"}, CWD, EXTRA)
