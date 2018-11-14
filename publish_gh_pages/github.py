
import os
from github3 import GitHub, GitHubEnterprise
from dotenv import load_dotenv
from IPython.display import display


class Github:
    """
    """

    def __init__(self,
                 url_github='https://github.com'):
        """
        Create Github object
        Enterprise or public Github (default)
        Auth from token if available
        Else from username/pwd
        """

        self.url_github = url_github

        load_dotenv(dotenv_path='credentials.env')

        username = os.environ.get('github-username')
        password = os.environ.get('github-password')
        token = os.environ.get('github-token')

        if url_github == 'https://github.com':
            if (token is not None):
                self.api = GitHub(token=token)
                self.test_connection('Wrong username/password')

            elif (username is not None) and (password is not None):
                self.api = GitHub(username=username,
                                  password=password)
                self.test_connection('Scopes must be "read:user, repo" at least')

            else:
                raise Exception(
                    'No credentials provided: They should be in a "credentials.env" file')
        else:
            if (token is not None):
                self.api = GitHubEnterprise(url=url_github,
                                            token=token)
                self.test_connection('Wrong username/password')

            elif (username is not None) and (password is not None):
                self.api = GitHubEnterprise(url=url_github,
                                            username=username,
                                            password=password)
                self.test_connection('Scopes must be "read:user, repo" at least')

            else:
                raise Exception(
                    'No credentials provided: They should be in a "credentials.env" file')

    def test_connection(self, message):
        """
        """
        print('testing connection to {}'.format(self.url_github))
        try:
            self.api.me()
        except:
            raise Exception(message)

    def load_repo(self,
                  orga_name,
                  repo_name):
        """
        """
        self.repo = self.api.repository(orga_name, repo_name)

    def create_file(self,
                    path=None,
                    message=None,
                    content=None,
                    branch=None):
        """
        """
        li_branch = [e.name for e in self.repo.branches()]
        assert branch in li_branch, 'branch {} does not exist'.format(branch)

        try:
            res = self.repo.create_file(path=path,
                                        message=message,
                                        content=content,
                                        branch=branch)
            print('file {} created'.format(path))
            return res

        except Exception as e:
            raise Exception('create_file failed: {}'.format(e))

    def update_file(self,
                    path=None,
                    message=None,
                    content=None,
                    branch=None):
        """
        """
        dir_contents = self.repo.directory_contents('.',
                                                    return_as=dict,
                                                    ref=branch)
        target_file = dir_contents[path]

        try:
            res = target_file.update(message,
                                     content,
                                     branch=branch)
            print('file {} updated'.format(path))
            return res

        except Exception as e:
            raise Exception('create_file failed: {}'.format(e))
