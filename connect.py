import pymysql
import vk
import top_secret

class DB:
    def __init__(self):
        self.db = pymysql.connect(host=top_secret.host, user=top_secret.user, passwd=top_secret.passwd,
                                  db=top_secret.db,
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.commit()
        self.db.close()

    def get_current_link_and_date(self):
        req = 'SELECT * from `last_edit` ORDER BY `date` DESC LIMIT 1;';
        self.cursor.execute(req)
        a = self.cursor.fetchone()
        a = a if a is not None else (None, None)
        return a

    def update_link(self, date, link):
        """
        True, если ссылка новая
        """
        l_date, l_link = self.get_current_link_and_date()
        if date != l_date or link != l_link:
            req = 'DELETE from last_edit;'
            self.cursor.execute(req)
            req = 'INSERT INTO `last_edit` (`date`,`link`) VALUES (\'' + str(date) + "','" + str(link) + '\');';
            self.cursor.execute(req)
            return True

    def has_user_with_id(self,user_id):
        req = 'SELECT * from `users` where id='+str(user_id)+";";
        self.cursor.execute(req)
        a = self.cursor.fetchone()
        return a is not None


    def check_last_msg(self,user_id,last_msg):
        """
        True, если последнее сообщение изменилось
        если юзера с таким id нет, то он создается
        """
        if self.has_user_with_id(user_id):
            req = "SELECT * from `users` where `id`=%d  and date(`last_msg`)<'%s';"  % (user_id,last_msg);
            self.cursor.execute(req)
            a = self.cursor.fetchone()
            if a is not None:
                req = "update `users` set `last_msg`='%s' where `id`=%d" % (last_msg, user_id)
                self.cursor.execute(req)
            return a is not None
        else:
            req = "insert into `users` (`id`,`last_msg`) values (%d,'%s')" % (user_id,last_msg)
            self.cursor.execute(req)
            return True

if __name__ == '__main__':
    db = DB()
    print(db.check_last_msg(3,'2018-09-01 15:40:08'))
