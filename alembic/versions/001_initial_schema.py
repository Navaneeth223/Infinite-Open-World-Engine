from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'worlds',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('seed', sa.BigInteger(), nullable=False),
        sa.Column('lore', sa.Text()),
        sa.Column('calendar_system', sa.JSON()),
        sa.Column('current_date', sa.JSON()),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('NOW()')),
    )


def downgrade():
    op.drop_table('worlds')
