from blog.models import EntryVotes, CommentVotes, Entry, Comment


class Votes():

    def __calculate_rate(self, vote_list):
        rate = 0

        for vote in vote_list:
            if vote.positive:
                rate += 1
            else:
                rate -= 1

        return rate

    # Checks if the user has voted the entry
    def __has_voted_entry(self, user_id, entry_id):
        nvotes = EntryVotes.objects.filter(
            user=user_id, entry=entry_id).count()
        if nvotes > 0:
            return True
        return False

    # Checks if the user has voted the comment
    def __has_voted_comment(self, user_id, comment_id):
        nvotes = CommentVotes.objects.filter(
            user=user_id, comment=comment_id).count()
        if nvotes > 0:
            return True
        return False

    # Checks if the user is the comment author
    def __is_comment_owner(self, user_id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if comment.author == user_id:
            return True
        return False

    def validate_entry_vote(self, user_id, entry_id):
        if self.__has_voted_entry(user_id, entry_id):
            return False
        return True

    def validate_comment_vote(self, user_id, comment_id):
        if (self.__has_voted_comment(user_id, comment_id)
                or self.__is_comment_owner(user_id, comment_id)):
            return False
        return True

    def set_entry_rate(self, post_id):
        votes = EntryVotes.objects.filter(entry=post_id)
        entry = Entry.objects.get(id=post_id)

        entry.rate = self.__calculate_rate(votes)
        entry.save()

    def set_comment_rate(self, comment_id):
        votes = CommentVotes.objects.filter(comment=comment_id)
        comment = Comment.objects.get(id=comment_id)

        comment.rate = self.__calculate_rate(votes)
        comment.save()
