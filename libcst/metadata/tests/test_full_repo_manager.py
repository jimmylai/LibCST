# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict
import json
from pathlib import Path
from unittest.mock import Mock, patch

from libcst.metadata.full_repo_manager import FullRepoManager
from libcst.metadata.tests.test_type_inference_provider import _test_simple_class_helper
from libcst.metadata.type_inference_provider import TypeInferenceProvider
from libcst.testing.utils import UnitTest


REPO_ROOT_DIR: str = str(Path(__file__).parent.parent.parent.resolve())


class FullRepoManagerTest(UnitTest):
    @patch.object(FullRepoManager, "_handle_pyre_cache")
    def test_get_metadata_wrapper_with_empty_cache(self, mocked_handler: Mock) -> None:
        path = "tests/pyre/simple_class.py"
        mocked_handler.return_value = {path: {"types": []}}
        manager = FullRepoManager(REPO_ROOT_DIR, [], [TypeInferenceProvider])
        wrapper = manager.get_metadata_wrapper_for_path(path)
        self.assertEqual(wrapper.resolve(TypeInferenceProvider), {})

    @patch.object(FullRepoManager, "_handle_pyre_cache")
    def test_get_metadata_wrapper_with_patched_cache(
        self, mocked_handler: Mock
    ) -> None:
        path_prefix = "tests/pyre/simple_class"
        path = f"{path_prefix}.py"
        mocked_handler.return_value = {
            path: json.loads((Path(REPO_ROOT_DIR) / f"{path_prefix}.json").read_text())
        }
        manager = FullRepoManager(REPO_ROOT_DIR, [], [TypeInferenceProvider])
        wrapper = manager.get_metadata_wrapper_for_path(path)
        _test_simple_class_helper(self, wrapper)
