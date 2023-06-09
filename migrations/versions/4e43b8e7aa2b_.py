"""empty message

Revision ID: 4e43b8e7aa2b
Revises: 
Create Date: 2023-05-05 21:19:28.121371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e43b8e7aa2b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('code',
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('expire', sa.DateTime(), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('follow',
    sa.Column('follower', sa.Integer(), nullable=False),
    sa.Column('followed', sa.Integer(), nullable=False),
    sa.Column('accept', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('password', sa.String(length=60), nullable=True),
    sa.Column('phone', sa.String(length=13), nullable=True),
    sa.Column('login_attempt', sa.Integer(), nullable=True),
    sa.Column('private', sa.Boolean(), nullable=True),
    sa.Column('phone_show', sa.Boolean(), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post',
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.Column('update_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('user')
    op.drop_table('follow')
    op.drop_table('code')
    # ### end Alembic commands ###
