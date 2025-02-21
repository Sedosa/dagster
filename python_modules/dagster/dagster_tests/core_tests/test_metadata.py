from dagster import NodeInvocation
from dagster._core.definitions.decorators import op
from dagster._legacy import PipelineDefinition, execute_pipeline


def test_solid_instance_tags():
    called = {}

    @op(tags={"foo": "bar", "baz": "quux"})
    def metadata_solid(context):
        assert context.solid.tags == {"foo": "oof", "baz": "quux", "bip": "bop"}
        called["yup"] = True

    pipeline = PipelineDefinition(
        name="metadata_pipeline",
        solid_defs=[metadata_solid],
        dependencies={
            NodeInvocation(
                "metadata_solid",
                alias="aliased_metadata_solid",
                tags={"foo": "oof", "bip": "bop"},
            ): {}
        },
    )

    result = execute_pipeline(
        pipeline,
    )

    assert result.success
    assert called["yup"]
