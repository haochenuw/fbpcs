/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#pragma once

#include <gflags/gflags_declare.h>

DECLARE_int32(party);
DECLARE_string(server_ip);
DECLARE_int32(port);
DECLARE_string(input_base_path_secret_share);
DECLARE_string(input_base_path);
DECLARE_string(output_base_path);
DECLARE_double(delta);
DECLARE_double(eps);
DECLARE_string(run_name);
DECLARE_bool(log_cost);
DECLARE_bool(add_dp_noise);
DECLARE_string(log_cost_s3_bucket);
DECLARE_string(log_cost_s3_region);
DECLARE_bool(use_tls);
DECLARE_string(ca_cert_path);
DECLARE_string(server_cert_path);
DECLARE_string(private_key_path);
DECLARE_int32(input_encryption);
DECLARE_int32(max_num_touchpoints);
DECLARE_int32(max_num_conversions);
DECLARE_bool(use_new_output_format);
DECLARE_int32(ciphertext_size);
DECLARE_int32(plaintext_size);
DECLARE_int32(decryption_table_size);
