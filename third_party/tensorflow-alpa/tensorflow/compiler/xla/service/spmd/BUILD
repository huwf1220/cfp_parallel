# Description: SPMD partitioning pass.

load("//tensorflow/tsl/platform:rules_cc.bzl", "cc_library")
load("//tensorflow:tensorflow.bzl", "tf_cc_test")
load(
    "//tensorflow/tsl/platform:build_config.bzl",
    "tf_proto_library",
)
load("//tensorflow/tsl/platform/default:build_config.bzl", "tf_proto_library_py",)
load("//tensorflow/compiler/xla:xla.bzl", "xla_py_proto_library")

package(
    default_visibility = [":friends"],
    licenses = ["notice"],
)

package_group(
    name = "friends",
    includes = [
        "//tensorflow/compiler/xla:friends",
    ],
)

tf_proto_library(
    name = "reindex_proto",
    visibility = ["//visibility:public"],
    srcs = ["reindexing.proto"],
    cc_api_version = 2,
)

cc_library(
    name = "spmd_partitioner",
    srcs = [
        "convolution_handler.cc",
        "custom_call_handler.cc",
        "dot_handler.cc",
        "fft_handler.cc",
        "gather_scatter_handler.cc",
        "spmd_partitioner.cc",
        "spmd_partitioner_util.cc",
    ],
    hdrs = [
        "convolution_handler.h",
        "custom_call_handler.h",
        "spmd_partitioner.h",
        "spmd_partitioner_util.h",
    ],
    deps = [
        "//tensorflow/compiler/xla:comparison_util",
        "//tensorflow/compiler/xla:literal_util",
        "//tensorflow/compiler/xla:protobuf_util",
        "//tensorflow/compiler/xla:shape_util",
        "//tensorflow/compiler/xla:status",
        "//tensorflow/compiler/xla:util",
        "//tensorflow/compiler/xla:window_util",
        "//tensorflow/compiler/xla:xla_data_proto_cc",
        "//tensorflow/compiler/xla/client:xla_builder",
        "//tensorflow/compiler/xla/client/lib:comparators",
        "//tensorflow/compiler/xla/service:call_graph",
        "//tensorflow/compiler/xla/service:custom_call_sharding_helper",
        "//tensorflow/compiler/xla/service:dot_as_convolution_util",
        "//tensorflow/compiler/xla/service:flatten_call_graph",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_cse",
        "//tensorflow/compiler/xla/service:hlo_dce",
        "//tensorflow/compiler/xla/service:hlo_lexer",
        "//tensorflow/compiler/xla/service:hlo_pass",
        "//tensorflow/compiler/xla/service:hlo_pass_pipeline",
        "//tensorflow/compiler/xla/service:hlo_query",
        "//tensorflow/compiler/xla/service:hlo_reachability",
        "//tensorflow/compiler/xla/service:hlo_sharding_util",
        "//tensorflow/compiler/xla/service:pattern_matcher",
        "//tensorflow/compiler/xla/service:shape_inference",
        "//tensorflow/compiler/xla/service:sharding_propagation",
        "//tensorflow/compiler/xla/service:tuple_simplifier",
        "//tensorflow/compiler/xla/stream_executor/lib",
        "//tensorflow/core:lib",
        "//tensorflow/tsl/platform:logging",
        "//tensorflow/tsl/platform:numbers",
        "@com_google_absl//absl/algorithm:container",
        "@com_google_absl//absl/cleanup",
        "@com_google_absl//absl/container:flat_hash_map",
        "@com_google_absl//absl/container:flat_hash_set",
        "@com_google_absl//absl/container:inlined_vector",
        "@com_google_absl//absl/container:node_hash_map",
        "@com_google_absl//absl/strings",
        "@com_google_absl//absl/types:span",
    ],
)

tf_cc_test(
    name = "spmd_partitioner_test",
    srcs = ["spmd_partitioner_test.cc"],
    deps = [
        ":spmd_partitioner",
        "//tensorflow/compiler/xla:util",
        "//tensorflow/compiler/xla:xla_data_proto_cc",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_matchers",
        "//tensorflow/compiler/xla/service:hlo_parser",
        "//tensorflow/compiler/xla/service:hlo_pass_pipeline",
        "//tensorflow/compiler/xla/service:hlo_sharding_util",
        "//tensorflow/compiler/xla/service:hlo_verifier",
        "//tensorflow/compiler/xla/service:sharding_propagation",
        "//tensorflow/compiler/xla/tests:hlo_test_base",
        "//tensorflow/compiler/xla/tests:xla_internal_test_main",
        "//tensorflow/tsl/lib/core:status_test_util",
        "//tensorflow/tsl/platform:test",
        "@com_google_absl//absl/algorithm:container",
    ],
)

tf_cc_test(
    name = "canonicalize_all_gather_for_cse_test",
    srcs = ["canonicalize_all_gather_for_cse_test.cc"],
    deps = [
        ":canonicalize_all_gather_for_cse",
        "//tensorflow/compiler/xla:xla_data_proto_cc",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_matchers",
        "//tensorflow/compiler/xla/service:hlo_parser",
        "//tensorflow/compiler/xla/service:hlo_pass_pipeline",
        "//tensorflow/compiler/xla/service:hlo_verifier",
        "//tensorflow/compiler/xla/tests:hlo_test_base",
        "//tensorflow/compiler/xla/tests:xla_internal_test_main",
        "//tensorflow/tsl/lib/core:status_test_util",
        "//tensorflow/tsl/platform:test",
    ],
)

cc_library(
    name = "canonicalize_all_gather_for_cse",
    srcs = ["canonicalize_all_gather_for_cse.cc"],
    hdrs = ["canonicalize_all_gather_for_cse.h"],
    deps = [
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_pass",
        "//tensorflow/compiler/xla/service:hlo_query",
        "@com_google_absl//absl/types:span",
    ],
)

tf_cc_test(
    name = "schedule_aware_collective_ops_cse_test",
    srcs = ["schedule_aware_collective_ops_cse_test.cc"],
    deps = [
        ":schedule_aware_collective_ops_cse",
        "//tensorflow/compiler/xla:xla_data_proto_cc",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_matchers",
        "//tensorflow/compiler/xla/service:hlo_parser",
        "//tensorflow/compiler/xla/service:hlo_pass_pipeline",
        "//tensorflow/compiler/xla/service:hlo_verifier",
        "//tensorflow/compiler/xla/tests:hlo_test_base",
        "//tensorflow/compiler/xla/tests:xla_internal_test_main",
        "//tensorflow/tsl/lib/core:status_test_util",
        "//tensorflow/tsl/platform:test",
    ],
)

cc_library(
    name = "schedule_aware_collective_ops_cse",
    srcs = ["schedule_aware_collective_ops_cse.cc"],
    hdrs = ["schedule_aware_collective_ops_cse.h"],
    deps = [
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_pass",
        "//tensorflow/compiler/xla/stream_executor/lib",
        "@com_google_absl//absl/container:flat_hash_map",
    ],
)

cc_library(
    name = "stateful_rng_spmd_partitioner",
    srcs = ["stateful_rng_spmd_partitioner.cc"],
    hdrs = ["stateful_rng_spmd_partitioner.h"],
    deps = [
        ":auto_sharding",
        ":spmd_partitioner",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_pass",
        "@com_google_absl//absl/memory",
    ],
)

tf_cc_test(
    name = "stateful_rng_spmd_partitioner_test",
    srcs = ["stateful_rng_spmd_partitioner_test.cc"],
    deps = [
        ":stateful_rng_spmd_partitioner",
        "//tensorflow/compiler/xla:util",
        "//tensorflow/compiler/xla:xla_data_proto_cc",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_matchers",
        "//tensorflow/compiler/xla/service:hlo_parser",
        "//tensorflow/compiler/xla/service:hlo_pass_pipeline",
        "//tensorflow/compiler/xla/service:hlo_verifier",
        "//tensorflow/compiler/xla/service:rng_expander",
        "//tensorflow/compiler/xla/service:sharding_propagation",
        "//tensorflow/compiler/xla/tests:hlo_test_base",
        "//tensorflow/compiler/xla/tests:xla_internal_test_main",
        "//tensorflow/tsl/lib/core:status_test_util",
        "//tensorflow/tsl/platform:test",
    ],
)

cc_library(
    name = "auto_sharding",
    srcs = ["auto_sharding.cc", "auto_sharding_util.cc", "auto_sharding_dot_handler.cc", "auto_sharding_opt_exp.cc"],
    hdrs = ["auto_sharding.h", "auto_sharding_strategy.h", "auto_sharding_util.h", "auto_sharding_opt_exp.h"],
    deps = [
        "//tensorflow/compiler/xla:shape_util",
        "//tensorflow/compiler/xla/service:dump",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_creation_utils",
        "//tensorflow/compiler/xla/service:hlo_live_range",
        "//tensorflow/compiler/xla/service:hlo_memory_scheduler",
        "//tensorflow/compiler/xla/service:hlo_pass",
        "//tensorflow/compiler/xla/service:hlo_sharding_util",
        "//tensorflow/compiler/xla/service:pass_context",
        ":reindex_proto_cc", 
        "@pybind11",
    ],
)

cc_library(
    name = "redundant_slice_eliminator",
    srcs = ["redundant_slice_eliminator.cc"],
    hdrs = ["redundant_slice_eliminator.h"],
    deps = [
        "//tensorflow/compiler/xla:shape_util",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_dce",
        "//tensorflow/compiler/xla/service:hlo_pass",
    ],
)

cc_library(
    name = "grad_acc_rewrite",
    srcs = ["grad_acc_rewrite.cc"],
    hdrs = ["grad_acc_rewrite.h"],
    deps = [
        "//tensorflow/compiler/xla:shape_util",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_pass",
        "//tensorflow/compiler/xla/service:pass_context",
        "//tensorflow/compiler/xla/service/spmd:spmd_partitioner",
    ],
)

cc_library(
    name = "slice_auto_sharded_stages",
    srcs = ["slice_auto_sharded_stages.cc"],
    hdrs = ["slice_auto_sharded_stages.h"],
    deps = [
        ":auto_sharding",
        "//tensorflow/compiler/xla:shape_util",
        "//tensorflow/compiler/xla/service:hlo",
        "//tensorflow/compiler/xla/service:hlo_pass",
        "@pybind11",
    ],
)

cc_library(
    name = "alpa_compiler",
    srcs = ["alpa_compiler.cc"],
    hdrs = ["alpa_compiler.h"],
    deps = [
        ":auto_sharding",
        ":redundant_slice_eliminator",
        ":grad_acc_rewrite",
        ":slice_auto_sharded_stages",
        ":stateful_rng_spmd_partitioner",
        # Copied from gpu_compiler
        "//tensorflow/compiler/xla/pjrt:pjrt_client",
        "//tensorflow/compiler/xla/service:algebraic_simplifier",
        "//tensorflow/compiler/xla/service:all_reduce_reassociate",
        "//tensorflow/compiler/xla/service:call_inliner",
        "//tensorflow/compiler/xla/service:conditional_canonicalizer",
        "//tensorflow/compiler/xla/service:conditional_simplifier",
        "//tensorflow/compiler/xla/service:dot_decomposer",
        "//tensorflow/compiler/xla/service:dot_merger",
        "//tensorflow/compiler/xla/service:dump",
        "//tensorflow/compiler/xla/service:gather_expander",
        "//tensorflow/compiler/xla/service:gather_simplifier",
        "//tensorflow/compiler/xla/service:hlo_constant_folding",
        "//tensorflow/compiler/xla/service:hlo_constant_splitter",
        "//tensorflow/compiler/xla/service:hlo_cse",
        "//tensorflow/compiler/xla/service:hlo_dce",
        "//tensorflow/compiler/xla/service:hlo_pass",
        "//tensorflow/compiler/xla/service:hlo_pass_pipeline",
        "//tensorflow/compiler/xla/service:hlo_verifier",
        "//tensorflow/compiler/xla/service:reshape_mover",
        "//tensorflow/compiler/xla/service:scatter_expander",
        "//tensorflow/compiler/xla/service:scatter_simplifier",
        "//tensorflow/compiler/xla/service:sharding_propagation",
        "//tensorflow/compiler/xla/service:sharding_remover",
        "//tensorflow/compiler/xla/service:sort_simplifier",
        "//tensorflow/compiler/xla/service:transpose_folding",
        "//tensorflow/compiler/xla/service:tuple_simplifier",
        "//tensorflow/compiler/xla/service:while_loop_constant_sinking",
        "//tensorflow/compiler/xla/service:while_loop_simplifier",
        "//tensorflow/compiler/xla/service:zero_sized_hlo_elimination",
        "//tensorflow/compiler/xla/service/gpu:gpu_conv_rewriter",
        "//tensorflow/compiler/xla/service/gpu:gpu_shape_verifier",
        "//tensorflow/compiler/xla/service/gpu:matmul_utils",
    ]
)
