from rest_framework import serializers

from tag.models import Tag
from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'author',
            'category',
            'tags',
            'public',
            'preparation',
            'tag_links'
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True
    )
    preparation = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(
        read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipe_api_v2_tag',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        super_validate = super().validate(attrs)

        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError({
                'title': ['Title and Description must be different.'],
                'description': ['Title and Description must be different.'],
            })

        return super_validate

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                'Title must have at least 5 chars.'
            )

        return value
