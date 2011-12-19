from darioblog.blog.models import EntryVotes, CommentVotes, Entry, Comment


class Votes():
    
    def __calculateRate(self, vote_list):
        rate = 0

        for vote in vote_list :
            if vote.positive :
                rate += 1
            else :
                rate -= 1

        return rate
    

    # Checks if the user has voted the entry
    def __hasVotedEntry(self, user_id, entry_id):
        nVotes = EntryVotes.objects.filter(user = user_id, entry = entry_id).count()
        if nVotes > 0 :
            return True
        return False


    # Checks if the user has voted the comment
    def __hasVotedComment(self, user_id, comment_id):
        nVotes = CommentVotes.objects.filter(user = user_id, comment = comment_id).count()
        if nVotes > 0:
            return True
        return False


    # Checks if the user is the comment author
    def __isCommentOwner(self, user_id, comment_id):
        comment = Comment.objects.get(id = comment_id)
        if comment.author == user_id:
            return True
        return False


    def validateEntryVote(self, user_id, entry_id):
        if self.__hasVotedEntry(user_id, entry_id):
            return False
        return True


    def validateCommentVote(self, user_id, comment_id):
        if self.__hasVotedComment(user_id, comment_id) or self.__isCommentOwner(user_id, comment_id) :
            return False
        return True


    def setEntryRate(self, post_id):
        votes = EntryVotes.objects.filter(entry = post_id)
        entry = Entry.objects.get(id = post_id)

        entry.rate = self.__calculateRate(votes)
        entry.save()


    def setCommentRate(self, comment_id):
        votes = CommentVotes.objects.filter(comment = comment_id)
        comment = Comment.objects.get(id = comment_id)

        comment.rate = self.__calculateRate(votes)
        comment.save()

