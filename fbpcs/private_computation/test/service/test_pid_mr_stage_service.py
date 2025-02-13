#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from fbpcs.common.entity.stage_state_instance import StageStateInstance
from fbpcs.private_computation.entity.infra_config import (
    InfraConfig,
    PrivateComputationGameType,
)
from fbpcs.private_computation.entity.private_computation_instance import (
    PrivateComputationInstance,
    PrivateComputationInstanceStatus,
    PrivateComputationRole,
)
from fbpcs.private_computation.entity.product_config import (
    CommonProductConfig,
    LiftConfig,
    ProductConfig,
)
from fbpcs.private_computation.service.pid_mr_stage_service import (
    PID_RUN_CONFIGS,
    PID_WORKFLOW_CONFIGS,
    PIDMR,
    PIDMRStageService,
    SPARK_CONFIGS,
)
from fbpcs.private_computation.stage_flows.private_computation_mr_stage_flow import (
    PrivateComputationMRStageFlow,
)
from fbpcs.service.workflow import WorkflowStatus
from fbpcs.service.workflow_sfn import SfnWorkflowService


class TestPIDMRStageService(IsolatedAsyncioTestCase):
    @patch("fbpcs.private_computation.service.pid_mr_stage_service.PIDMRStageService")
    async def test_run_async(self, pid_mr_svc_mock) -> None:
        for test_run_id in (None, "2621fda2-0eca-11ed-861d-0242ac120002"):
            with self.subTest(test_run_id=test_run_id):
                flow = PrivateComputationMRStageFlow
                infra_config: InfraConfig = InfraConfig(
                    instance_id="publisher_123",
                    role=PrivateComputationRole.PUBLISHER,
                    status=PrivateComputationInstanceStatus.PID_MR_STARTED,
                    status_update_ts=1600000000,
                    instances=[],
                    game_type=PrivateComputationGameType.LIFT,
                    num_pid_containers=1,
                    num_mpc_containers=1,
                    num_files_per_mpc_container=1,
                    status_updates=[],
                    _stage_flow_cls_name=flow.get_cls_name(),
                    run_id=test_run_id,
                )
                common: CommonProductConfig = CommonProductConfig(
                    input_path="https://mpc-aem-exp-platform-input.s3.us-west-2.amazonaws.com/pid_test_data/stress_test/input.csv",
                    output_dir="https://mpc-aem-exp-platform-input.s3.us-west-2.amazonaws.com/pid_test/output",
                    pid_configs={
                        PIDMR: {
                            PID_WORKFLOW_CONFIGS: {"state_machine_arn": "machine_arn"},
                            PID_RUN_CONFIGS: {"conf": "conf1"},
                            SPARK_CONFIGS: {"conf-2": "conf2"},
                        }
                    },
                )
                product_config: ProductConfig = LiftConfig(
                    common=common,
                )

                pc_instance = PrivateComputationInstance(
                    infra_config=infra_config,
                    product_config=product_config,
                )

                service = SfnWorkflowService("us-west-2", "access_key", "access_data")
                service.start_workflow = MagicMock(return_value="execution_arn")
                service.get_workflow_status = MagicMock(
                    return_value=WorkflowStatus.COMPLETED
                )
                stage_svc = PIDMRStageService(
                    service,
                )
                await stage_svc.run_async(pc_instance)

                self.assertEqual(
                    stage_svc.get_status(pc_instance),
                    PrivateComputationInstanceStatus.PID_MR_COMPLETED,
                )
                self.assertEqual(
                    pc_instance.pid_mr_stage_output_data_path,
                    "https://mpc-aem-exp-platform-input.s3.us-west-2.amazonaws.com/pid_test/output/publisher_123_out_dir/pid_mr",
                )
                self.assertEqual(
                    pc_instance.infra_config.instances[0].instance_id, "execution_arn"
                )
                self.assertIsInstance(
                    pc_instance.infra_config.instances[0], StageStateInstance
                )
