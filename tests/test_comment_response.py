from src.repository.comments import get_comment, update_comment, delete_comment
from src.database.models import Comment
import unittest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
import sys
import os

sys.path.append(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))


class TestAsyncMethod(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        """Set up an AsyncMock for the database session."""
        self.session = AsyncMock(spec=AsyncSession())

    async def asyncTearDown(self) -> None:
        """Tear down the AsyncMock for the database session."""
        del self.session

    async def test_get_comment(self):
        """Test the get_comment method."""
        comment_id = 1
        comment_text = 'This is a test comment'
        mock_comment = Comment(id=comment_id, text=comment_text)
        self.session.get.return_value = mock_comment

        result = await get_comment(comment_id, self.session)

        self.assertEqual(result, mock_comment)
        self.session.get.assert_called_once_with(Comment, comment_id)

    async def test_update_comment(self):
        """Test the update_comment method."""
        comment_id = 1
        new_comment_text = 'Update comment text'
        mock_comment = Comment(
            id=comment_id, text='Original comment text', update_status=False
        )
        self.session.get.return_value = mock_comment

        result = await update_comment(new_comment_text, comment_id, self.session)

        self.assertEqual(result.text, new_comment_text)
        self.assertEqual(result.update_status, True)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(mock_comment)

    async def test_delete_comment(self):
        """Test the delete_comment method."""
        comment_id = 1
        mock_comment = Comment(id=comment_id, text='Test comment')
        self.session.get.return_value = mock_comment

        result = await delete_comment(comment_id, self.session)

        self.assertEqual(result, mock_comment)
        self.session.delete.assert_called_once_with(mock_comment)
        self.session.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
