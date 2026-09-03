# src/ota_installer/task/task_group_pipelines.py
from dataclasses import dataclass
from functools import partial


@dataclass(frozen=True, slots=True)
class Pipeline:
    steps: tuple

    def get(self, name: str) -> Step:
        for step in self.steps:
            if step.name == name:
                return step

        raise KeyError(f"Pipeline step does not exist: {name}")

    def __getitem__(self, index: int) -> Step:
        return self.steps[index]


@dataclass(frozen=True, slots=True)
class Step:
    name: str
    index: int
    title: str
    description: str
    command_string: str | None = None
    reminder: str | None = None

    @property
    def success_message(self) -> str:
        from ..style.style_renderer import indentation

        return (
            f"{indentation(2)}"
            f"{self.name.lower().replace('_', ' ').capitalize()} "
            "finished successfully!"
        )


PREPARATION = Pipeline(
    steps=(
        Step(
            name="extract_payload_image",
            index=1,
            title="Payload Image Extractor",
            description="📦 Extracting payload.bin to access OTA image files.",
        ),
        Step(
            name="rename_payload_image",
            index=2,
            title="Payload Image Renamer",
            description="📝 Renaming the extracted image file for clarity.",
        ),
        Step(
            name="extract_stock_boot_image",
            index=3,
            title="Boot Image Extractor",
            description="🪄  Pulling the boot image from the OTA payload.",
        ),
        Step(
            name="backup_stock_boot_image",
            index=4,
            title="Backup Stock Boot Image",
            description="📁 Backing up your stock boot image.",
        ),
    )
)

MIGRATION = Pipeline(
    steps=(
        Step(
            name="check_adb_connection",
            index=1,
            title="Check ADB Connection",
            description="🔌 Checking for an ADB-connected device.",
            command_string="adb devices",
        ),
        Step(
            name="push_stock_image",
            index=2,
            title="Push Stock Boot Image",
            description="📤 Pushing the stock boot image to your device.",
            reminder="Patch boot image in Magisk app",
        ),
        Step(
            name="find_magisk_image",
            index=3,
            title="Find Magisk Image",
            description="🔍 Searching for the patched Magisk image.",
        ),
        Step(
            name="pull_magisk_image",
            index=4,
            title="Pull Magisk Image",
            description="📥 Pulling the patched Magisk image to your computer.",
            command_string="",
            reminder="",
        ),
    )
)

APPLICATION = Pipeline(
    steps=(
        Step(
            name="reboot_to_recovery",
            index=1,
            title="Reboot To Recovery",
            description="♻️ Rebooting the device into recovery mode.",
            command_string="adb reboot recovery",
        ),
        Step(
            name="apply_ota_update",
            index=2,
            title="Apply OTA Image",
            description="🚀 Applying the OTA update via adb sideload.",
            reminder="Restart to verify build, then reboot to Bootloader",
        ),
        Step(
            name="reboot_to_bootloader",
            index=3,
            title="Reboot to Bootloader",
            description="🧰 Rebooting into bootloader (fastboot) mode.",
            command_string="adb reboot bootloader",
        ),
        Step(
            name="boot_to_magisk_image",
            index=4,
            title="Boot to Magisk Image",
            description="💾 Flashing the patched Magisk image with fastboot.",
        ),
    )
)


def get_step_names(pipeline: Pipeline) -> tuple[str, ...]:
    return tuple(step.name for step in pipeline.steps)


TASK_GROUPS = {
    "preparation": partial(get_step_names, PREPARATION),
    "migration": partial(get_step_names, MIGRATION),
    "application": partial(get_step_names, APPLICATION),
}
# Signed off by Brian Sanford on 20260903
