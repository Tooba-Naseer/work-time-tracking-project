from datetime import date
from operator import itemgetter

from rest_framework import serializers

from projects.models import ProjectTimeLog
from users.v1.serializers import UserSerializer
from .project import ProjectReadOnlySerializer


class ProjectTimeLogSerializer(serializers.ModelSerializer):
    """Serializer for Project Time Log"""

    duration = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        """
        Override to_representation in order to add project object in the response
        """

        data = super().to_representation(instance)
        data["project"] = ProjectReadOnlySerializer(instance.project).data

        return data

    def validate_date(self, value):
        """Validate the date"""

        if value > date.today():
            raise serializers.ValidationError("You cannot log time for future date")

        return value

    def validate_start_and_end_time(self, start_time, end_time):
        """Validate the start time and end time"""

        if end_time <= start_time:
            raise serializers.ValidationError(
                "End time should be greater than start time"
            )

        return

    def validate_existing_time_slots_for_same_day(
        self, user, work_date, start_time, end_time
    ):
        """
        Validate that whether existing time slot entries for the given date overlaps the new entry or not
        for that specific user.
        User cannot log the work time that overlaps.
        """

        time_slots = [(start_time, "s"), (end_time, "e")]
        if not self.instance:
            time_logs = ProjectTimeLog.objects.filter(user=user, date=work_date)
        else:
            time_logs = ProjectTimeLog.objects.filter(
                user=user, date=work_date
            ).exclude(id=self.instance.id)
        for time_log in time_logs:
            time_slots.append((time_log.start_time, "s"))
            time_slots.append((time_log.end_time, "e"))

        sorted_time_slots = sorted(time_slots, key=itemgetter(0, 1))
        for i in range(len(sorted_time_slots) - 1):
            if sorted_time_slots[i][1] == sorted_time_slots[i + 1][1] == "s":
                raise serializers.ValidationError(
                    "Time clash occurs. You cannot have work time slots that are overlapping."
                )

        return

    def validate(self, data):
        """Validate the incoming data"""

        user = self.context["request"].user
        # when there is a create request
        if not self.instance:
            start_time = data["start_time"]
            end_time = data["end_time"]
            work_date = data["date"]
        # when there is an update request
        else:
            start_time = data.get("start_time", self.instance.start_time)
            end_time = data.get("end_time", self.instance.end_time)
            work_date = data.get("date", self.instance.date)

        self.validate_start_and_end_time(start_time, end_time)
        self.validate_existing_time_slots_for_same_day(
            user, work_date, start_time, end_time
        )

        return data

    class Meta:
        model = ProjectTimeLog
        fields = "__all__"
        read_only_fields = ("user",)
