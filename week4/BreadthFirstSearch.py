import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        # 辞書からページタイトルをIDに変換
        start_id = next((id for id, title in self.titles.items() if title == start), None)
        goal_id = next((id for id, title in self.titles.items() if title == goal), None)
        if start_id is None or goal_id is None:
            return None

        queue = collections.deque([(start_id, [start_id])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            if current == goal_id:
                return [self.titles[p] for p in path]
            visited.add(current)
            for neighbor in self.links[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        num_nodes = len(self.titles)
        current_rank = [1.0 / num_nodes] * num_nodes
        updated_rank = [0.0] * num_nodes
        damping_factor = 0.85
        epsilon = 0.01  # 収束閾値

        while True:
            # ランクを更新するためのにリセット
            updated_rank = [0.0] * num_nodes

            # 各ページからのランクの分配
            for src in self.titles.keys():
                if self.links[src]:
                    shared_rank = damping_factor * current_rank[src] / len(self.links[src])
                else:
                    shared_rank = 0

                universal_rank = (1 - damping_factor) * current_rank[src] / num_nodes

                for dst in self.links[src]:
                    updated_rank[dst] += shared_rank

                for i in range(num_nodes):
                    updated_rank[i] += universal_rank

            sum_ranks = sum(updated_rank)
            updated_rank = [rank / sum_ranks for rank in updated_template]

            # 収束条件のチェック
            diff = sum(abs(updated_rank[i] - current_rank[i]) for i in range(num_nodes))
            if diff < epsilon:
                break

            current_rank = updated_rank

        # ランクが最も高いページトップ10を表示
        ranked_pages = sorted(((self.titles[id], rank) for id, rank in enumerate(current_rank)), key=lambda x: x[1],
                              reverse=True)[:10]
        print("Top 10 most popular pages:")
        for title, rank in ranked_pages:
            print(f"{title}: {rank}")


    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
