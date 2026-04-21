from apps.neuralapi.models import HopfieldExercise, HopfieldMachine
from library.redesneu.hopfield import Hopfield
from rest_framework import serializers
import numpy as np
import io

class MachineSerializer(serializers.ModelSerializer):
    training_data = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField()),
        write_only=True
    )
    
    class Meta:
        model = HopfieldMachine
        fields = ('id', 'name', 'dims', 'training_data', 'created_at')
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        patterns = np.array(validated_data.pop('training_data'))
        validated_data.pop('dims')
        
        machine = Hopfield(inputs=patterns)

        buffer = io.BytesIO()
        np.save(buffer, machine.weight)

        return HopfieldMachine.objects.create(
            weights=buffer.getvalue(),
            dims=machine.feature_size,
            **validated_data
        )   

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HopfieldExercise
        fields = ('id', 'machine', 'inputs', 'result', 'is_convergent', 'epochs', 'image')
        read_only_fields = ()
