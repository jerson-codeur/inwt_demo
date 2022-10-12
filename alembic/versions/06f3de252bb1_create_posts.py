"""create posts

Revision ID: 06f3de252bb1
Revises: 
Create Date: 2022-10-10 21:45:36.156062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06f3de252bb1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default= sa.text('now()')),
                    sa.Column('owner_id', sa.Integer(), nullable=False)
                    )
   
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
