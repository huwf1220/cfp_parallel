"""All global configurations for this project."""
import os
import psutil


class GlobalConfig:
    """The global configuration of alpa."""

    def __init__(self):
        ########## Options of device mesh ##########
        self.backend = "gpu"
        self.has_cuda = os.system("nvidia-smi > /dev/null 2>&1") == 0
        # See https://jax.readthedocs.io/en/latest/gpu_memory_allocation.html
        self.xla_client_mem_fraction = float(
            os.environ.get("XLA_PYTHON_CLIENT_MEM_FRACTION", 0.9))
        self.xla_gpu_autotune_level = 4
        # The threshold to tigger a batched deletion on workers.
        self.delete_remote_arrays_threshold = 50
        # Whether to use AWS EFA network interface
        self.use_aws_efa = os.environ.get("ALPA_USE_AWS_EFA",
                                          "").lower() in ["true", "1"]
        # Random seed used for compilation
        self.compile_random_seed = 42
        # Random seed used for runtime
        self.runtime_random_seed = 42

        ########## Options of shard_parallel ##########
        # Whether to sync before and after the executable for accurate internal
        # timer
        self.shard_parallel_sync_for_timer = False

        ########## Options of pipeline_parallel ##########
        # Whether to debug with pipeshard runtime. If turned on, no physical
        # resource is required until launching PipeshardExecutable.
        self.debug_with_pipeshard_runtime = False
        # Whether to use the whole cluster for stage profiling. If not, only
        # use the given mesh.
        self.profile_with_whole_ray_cluster = False
        # Stage construction profiling time threshold.
        self.profile_timeout = 500
        # Stage construction profiling retry threshold.
        # Some communication patterns may meet deadlock, so it needs retry.
        self.profile_maximum_retry = 2
        # Whether to forcely set stage construction's submesh choices
        self.overwrite_submesh_choices = None
        self.always_donate_micro_batch_vars = True

        ########## Options of pipeline runtime ##########
        self.pipeline_check_alive = False
        # Whether to sync before and after the executable for accurate internal
        # timer
        self.pipeline_sync_for_timer = False
        # Whether to use distributed compilation in pipeline parallel for
        # each stage. Disabling it helps debug.
        self.pipeline_distributed_compile = False
        # Whether to use single-byte signal tensor for send/recv.
        # This is a debug option.
        self.pipeline_use_signal_send_recv = False
        # Whether to use the scatter-gater/local-all-gather optimization.
        self.use_local_allgather = True
        self.eagerly_create_communicators = True
        # Cross mesh resharding mode. Possible choices: {"send_recv",
        # "broadcast"}
        self.resharding_mode = "send_recv"
        # Which nccl to use. Possible choices: {"cupy",
        # "xla_extension"}
        self.nccl_mode = "cupy"
        self.enable_overlapping = False

        ########## Options of benchmark ##########
        # If true, the system is allowed to use dummy values during
        # tensor creation and copy to reduce the initialization and copy time.
        # This will produce wrong results but is acceptable for
        # data-independent benchmarks.
        self.use_dummy_value_for_benchmarking = True

        ########## Options of monkey patch ##########
        self.flax_always_use_fp16_embedding = False

        ########## Options of logging ##########
        self.print_compilation_time = True
        self.print_auto_layer_stats = False

        # Whether to collect activity trace
        self.collect_trace = False

        self.MAX_MEM_SIZE = 40

    @property
    def ray_accelerator_name(self):
        backend_to_ray = {"gpu": "GPU"}
        return backend_to_ray[self.backend]

class ParallelCompileConfig:
    def __init__(self, threads_per_worker = 4, max_worker_num = 10):
        self.core_id_list = list(os.sched_getaffinity(os.getpid()))
        self.total_thread_num = len(self.core_id_list)
        self.threads = threads_per_worker
        self.worker_num = min(self.total_thread_num // self.threads, max_worker_num)
        self.best_cost = 1e+5
        assert(self.threads * self.worker_num <= 48)
    def sliced_compile_work(self, worker_idx, stras):
        start = worker_idx*(len(stras)//self.worker_num)
        end = min((worker_idx+1)*(len(stras)//self.worker_num), len(stras))
        return stras[start:end]
    def set_cpu_affinity(self, worker_idx):
        pid = os.getpid()
        p = psutil.Process(pid)
        first = self.threads*worker_idx
        p.cpu_affinity(self.core_id_list[first : first + self.threads])

global_config = GlobalConfig()
parallel_compile_config = ParallelCompileConfig()


# Other environment setup
is_worker = os.environ.get("ALPA_IS_WORKER", "False") == "True"

os.environ["XLA_FLAGS"] = (os.environ.get("XLA_FLAGS", "") +
                           " --xla_gpu_enable_async_all_reduce=false" +
                           " --xla_gpu_force_compilation_parallelism=8")

# add by huwf
CROSS_SEG_RESHARDING_BW = 32 * 10**9