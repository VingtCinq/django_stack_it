# Generated by Django 2.1.5 on 2019-03-15 10:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import mptt.fields
import polymorphic_tree.models
import stack_it.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('folder', models.CharField(choices=[('folder', 'folder')],
                                            default='folder', max_length=50, verbose_name='Folder')),
                ('image', models.ImageField(upload_to='', verbose_name='Image')),
                ('alt', models.CharField(blank=True, max_length=50, verbose_name='Alternative text')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('slug', models.SlugField(blank=True, verbose_name='Slug')),
                ('auto_slug', models.BooleanField(
                    default=True, help_text="When set, your slug will automatically be updated from field define in class's SLUGIFY_FROM", verbose_name='Auto Slug')),
                ('ref_full_path', models.SlugField(editable=False, unique=True, verbose_name='Denormalized full path')),
                ('template_path', models.CharField(default='', max_length=250, verbose_name='Template Path')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('status', model_utils.fields.StatusField(choices=[
                 ('draft', 'Draft'), ('published', 'published')], default='draft', max_length=100, no_check_for_status=True)),
                ('verbose_name', models.CharField(max_length=50, verbose_name='Instance model verbose_name')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', polymorphic_tree.models.PolymorphicTreeForeignKey(blank=True, null=True,
                                                                             on_delete=django.db.models.deletion.CASCADE, related_name='children', to='stack_it.Page')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                        related_name='polymorphic_stack_it.page_set+', to='contenttypes.ContentType')),
                ('sites', models.ManyToManyField(to='sites.Site', verbose_name='Site')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('key', models.CharField(max_length=50, verbose_name='Key')),
                ('content_type', models.CharField(choices=[
                 ('meta', 'Meta content'), ('value', 'Standard content')], default='value', max_length=50, verbose_name='Content Type')),
            ],
            options={
                'verbose_name': 'Page Content',
                'verbose_name_plural': 'Page Contents',
            },
        ),
        migrations.CreateModel(
            name='TemplateContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(
                    default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('key', models.CharField(max_length=50, verbose_name='Key')),
                ('content_type', models.CharField(choices=[
                 ('meta', 'Meta content'), ('value', 'Standard content')], default='value', max_length=50, verbose_name='Content Type')),
                ('path', models.CharField(db_index=True, max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Template',
            },
        ),
        migrations.CreateModel(
            name='ImagePageContent',
            fields=[
                ('pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                         parent_link=True, primary_key=True, serialize=False, to='stack_it.PageContent')),
                ('ref_image', models.ImageField(upload_to='', verbose_name='Image')),
                ('ref_alt', models.CharField(blank=True, max_length=50, null=True, verbose_name='Alternative text')),
                ('size', models.CharField(default='800x600', max_length=50, validators=[
                 stack_it.utils.validators.validate_image_size], verbose_name='Size')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            to='stack_it.Image', verbose_name='Image instance')),
            ],
            options={
                'verbose_name': 'Image Page Content',
                'verbose_name_plural': 'Image Page Contents',
            },
            bases=('stack_it.pagecontent', models.Model),
        ),
        migrations.CreateModel(
            name='ImageTemplateContent',
            fields=[
                ('templatecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                             parent_link=True, primary_key=True, serialize=False, to='stack_it.TemplateContent')),
                ('ref_image', models.ImageField(upload_to='', verbose_name='Image')),
                ('ref_alt', models.CharField(blank=True, max_length=50, null=True, verbose_name='Alternative text')),
                ('size', models.CharField(default='800x600', max_length=50, validators=[
                 stack_it.utils.validators.validate_image_size], verbose_name='Size')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            to='stack_it.Image', verbose_name='Image instance')),
            ],
            options={
                'verbose_name': 'Image Template Content',
                'verbose_name_plural': 'Image Template Contents',
            },
            bases=('stack_it.templatecontent', models.Model),
        ),
        migrations.CreateModel(
            name='ModelPageContent',
            fields=[
                ('pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                         parent_link=True, primary_key=True, serialize=False, to='stack_it.PageContent')),
                ('instance_id', models.IntegerField(null=True, verbose_name='Object id')),
                ('model_name', models.CharField(max_length=50, validators=[
                 stack_it.utils.validators.validate_model_name], verbose_name='Model Name')),
            ],
            options={
                'verbose_name': 'Related Model Page Content',
                'verbose_name_plural': 'Related Model Page Contents',
            },
            bases=('stack_it.pagecontent', models.Model),
        ),
        migrations.CreateModel(
            name='ModelTemplateContent',
            fields=[
                ('templatecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                             parent_link=True, primary_key=True, serialize=False, to='stack_it.TemplateContent')),
                ('instance_id', models.IntegerField(null=True, verbose_name='Object id')),
                ('model_name', models.CharField(max_length=50, validators=[
                 stack_it.utils.validators.validate_model_name], verbose_name='Model Name')),
            ],
            options={
                'verbose_name': 'Related Model Template Content',
                'verbose_name_plural': 'Related Model Template Contents',
            },
            bases=('stack_it.templatecontent', models.Model),
        ),
        migrations.CreateModel(
            name='PagePageContent',
            fields=[
                ('pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                         parent_link=True, primary_key=True, serialize=False, to='stack_it.PageContent')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='related_pagepagecontent', to='stack_it.Page', verbose_name='Page')),
            ],
            options={
                'verbose_name': 'Related Page Page Content',
                'verbose_name_plural': 'Related Page Page Contents',
            },
            bases=('stack_it.pagecontent', models.Model),
        ),
        migrations.CreateModel(
            name='PageTemplateContent',
            fields=[
                ('templatecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                             parent_link=True, primary_key=True, serialize=False, to='stack_it.TemplateContent')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='related_pagetemplatecontent', to='stack_it.Page', verbose_name='Page')),
            ],
            options={
                'verbose_name': 'Related Page Template Content',
                'verbose_name_plural': 'Related Page Template Contents',
            },
            bases=('stack_it.templatecontent', models.Model),
        ),
        migrations.CreateModel(
            name='TextPageContent',
            fields=[
                ('pagecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                         parent_link=True, primary_key=True, serialize=False, to='stack_it.PageContent')),
                ('value', models.TextField(verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Text Page Content',
                'verbose_name_plural': 'Text Page Contents',
            },
            bases=('stack_it.pagecontent', models.Model),
        ),
        migrations.CreateModel(
            name='TextTemplateContent',
            fields=[
                ('templatecontent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                             parent_link=True, primary_key=True, serialize=False, to='stack_it.TemplateContent')),
                ('value', models.TextField(verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Text Template Content',
                'verbose_name_plural': 'Text Template Contents',
            },
            bases=('stack_it.templatecontent', models.Model),
        ),
        migrations.AddField(
            model_name='templatecontent',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='polymorphic_stack_it.templatecontent_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='pagecontent',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='contents', to='stack_it.Page', verbose_name='Page'),
        ),
        migrations.AddField(
            model_name='pagecontent',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='polymorphic_stack_it.pagecontent_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='menu',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='menus', to='stack_it.Page', verbose_name='Page'),
        ),
        migrations.AddField(
            model_name='menu',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='stack_it.Menu'),
        ),
        migrations.AlterUniqueTogether(
            name='templatecontent',
            unique_together={('path', 'key')},
        ),
        migrations.AlterUniqueTogether(
            name='pagecontent',
            unique_together={('page', 'key')},
        ),
    ]
