import functools
import copy


def validate_decorator(**need_arg):
    '''
       参数验证装饰器
       :param need_arg: 需要验证的参数名称 包含参数类型,参数所需要有的属性或子参数
       :return:
    '''

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kw):
            for arg in need_arg:
                if not arg in kw:
                    raise ValueError('函数使用错误, 无参数%s' % (arg))
                func_arg = kw[arg]
                if func_arg == None:
                    continue
                arg_type = need_arg[arg]['type']
                if not isinstance(func_arg, arg_type):
                    raise ValueError('函数使用错误,参数类型错误')
                if 'must_arg' in need_arg[arg]:
                    must_arg = need_arg[arg]['must_arg']
                    if not isinstance(func_arg, (list, tuple)):
                        func_arg = [func_arg]

                    for item in func_arg:
                        must_arg_copy = copy.deepcopy(must_arg)

                        for a in item:
                            if a not in must_arg_copy:
                                raise ValueError('函数使用错误,%s 含有非法参数%s' % (arg, a))
                            else:
                                must_arg_copy.pop(a)
                        if len(must_arg_copy) > 0:
                            for i in must_arg_copy:
                                if must_arg_copy[i]:
                                    raise ValueError('函数使用错误,%s 缺少参数%s' % (arg, i))
            return func(*args, **kw)

        return wrapper

    return decorator


def timeoutFn(func, kwargs={}, timeout_duration=1, default=None):
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        print('time out')
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(**kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    return result


a = {'total_number': 20, 'hasvisible': False, 'statuses': [
    {'visible': {'type': 0, 'list_id': 0}, 'hasActionTypeCard': 0, 'userType': 0, 'id': 4211016852254679, 'geo': None,
     'comment_manage_info': {'approval_comment_type': 0, 'comment_manage_button': 1, 'comment_permission_type': 0},
     'text': 'Hihttp://t.cn/RHM3DwB \u200b', 'source_allowclick': 0, 'is_show_bulletin': 2, 'attitudes_count': 0,
     'hot_weibo_tags': [], 'truncated': False, 'can_edit': False, 'mid': '4211016852254679',
     'idstr': '4211016852254679', 'is_paid': False, 'reposts_count': 0, 'mblog_vip_type': 0,
     'in_reply_to_status_id': '', 'biz_feature': 0, 'more_info_type': 0, 'pic_urls': [], 'darwin_tags': [],
     'content_auth': 0, 'in_reply_to_user_id': '', 'source_type': 1, 'gif_ids': '',
     'created_at': 'Sat Feb 24 18:28:37 +0800 2018', 'text_tag_tips': [], 'textLength': 21, 'isLongText': False,
     'favorited': False, 'comments_count': 1, 'pending_approval_count': 0, 'positive_recom_flag': 0,
     'source': '<a href="http://app.weibo.com/t/feed/2W68oO" rel="nofollow">未通过审核应用</a>', 'mlevel': 0,
     'user': {'name': 'HiGDPU', 'avatar_large': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif',
              'followers_count': 13, 'allow_all_comment': True, 'ptype': 0, 'province': '100',
              'verified_source_url': '', 'idstr': '2203175032', 'mbrank': 0, 'domain': 'HiGDPU',
              'bi_followers_count': 0, 'credit_score': 80, 'story_read_state': -1, 'online_status': 0,
              'favourites_count': 5, 'star': 0, 'city': '1000', 'remark': '', 'mbtype': 0, 'verified_source': '',
              'block_app': 0, 'url': '', 'verified_reason_url': '', 'class': 1, 'verified': False, 'id': 2203175032,
              'profile_image_url': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_50.gif', 'urank': 6,
              'like': False, 'allow_all_act_msg': False, 'gender': 'm', 'location': '其他',
              'avatar_hd': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif', 'description': '',
              'weihao': '', 'screen_name': 'HiGDPU', 'follow_me': False, 'user_ability': 0, 'verified_trade': '',
              'vclub_member': 0, 'following': False, 'pagefriends_count': 0, 'block_word': 0, 'geo_enabled': True,
              'profile_url': 'HiGDPU', 'friends_count': 7, 'created_at': 'Wed Jun 29 11:20:30 +0800 2011',
              'lang': 'zh-cn', 'verified_type': -1, 'like_me': False, 'verified_reason': '',
              'insecurity': {'sexual_content': False}, 'statuses_count': 0}, 'in_reply_to_screen_name': ''},
    {'visible': {'type': 0, 'list_id': 0}, 'hasActionTypeCard': 0, 'userType': 0, 'id': 4211015451302258, 'geo': None,
     'comment_manage_info': {'approval_comment_type': 0, 'comment_manage_button': 1, 'comment_permission_type': 0},
     'text': 'Hihttp://t.cn/RHM3DwB \u200b', 'source_allowclick': 0, 'is_show_bulletin': 2, 'attitudes_count': 0,
     'hot_weibo_tags': [], 'truncated': False, 'can_edit': False, 'mid': '4211015451302258',
     'idstr': '4211015451302258', 'is_paid': False, 'reposts_count': 0, 'mblog_vip_type': 0,
     'in_reply_to_status_id': '', 'biz_feature': 0, 'more_info_type': 0, 'pic_urls': [], 'darwin_tags': [],
     'content_auth': 0, 'in_reply_to_user_id': '', 'source_type': 1, 'gif_ids': '',
     'created_at': 'Sat Feb 24 18:23:03 +0800 2018', 'text_tag_tips': [], 'textLength': 21, 'isLongText': False,
     'favorited': False, 'comments_count': 0, 'pending_approval_count': 0, 'positive_recom_flag': 0,
     'source': '<a href="http://app.weibo.com/t/feed/2W68oO" rel="nofollow">未通过审核应用</a>', 'mlevel': 0,
     'user': {'name': 'HiGDPU', 'avatar_large': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif',
              'followers_count': 13, 'allow_all_comment': True, 'ptype': 0, 'province': '100',
              'verified_source_url': '', 'idstr': '2203175032', 'mbrank': 0, 'domain': 'HiGDPU',
              'bi_followers_count': 0, 'credit_score': 80, 'story_read_state': -1, 'online_status': 0,
              'favourites_count': 5, 'star': 0, 'city': '1000', 'remark': '', 'mbtype': 0, 'verified_source': '',
              'block_app': 0, 'url': '', 'verified_reason_url': '', 'class': 1, 'verified': False, 'id': 2203175032,
              'profile_image_url': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_50.gif', 'urank': 6,
              'like': False, 'allow_all_act_msg': False, 'gender': 'm', 'location': '其他',
              'avatar_hd': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif', 'description': '',
              'weihao': '', 'screen_name': 'HiGDPU', 'follow_me': False, 'user_ability': 0, 'verified_trade': '',
              'vclub_member': 0, 'following': False, 'pagefriends_count': 0, 'block_word': 0, 'geo_enabled': True,
              'profile_url': 'HiGDPU', 'friends_count': 7, 'created_at': 'Wed Jun 29 11:20:30 +0800 2011',
              'lang': 'zh-cn', 'verified_type': -1, 'like_me': False, 'verified_reason': '',
              'insecurity': {'sexual_content': False}, 'statuses_count': 0}, 'in_reply_to_screen_name': ''},
    {'visible': {'type': 0, 'list_id': 0}, 'hasActionTypeCard': 0, 'userType': 0, 'id': 4211012830273589, 'geo': None,
     'comment_manage_info': {'approval_comment_type': 0, 'comment_manage_button': 1, 'comment_permission_type': 0},
     'text': 'Hihttp://t.cn/RHM3DwB \u200b', 'source_allowclick': 0, 'is_show_bulletin': 2, 'attitudes_count': 0,
     'hot_weibo_tags': [], 'truncated': False, 'can_edit': False, 'mid': '4211012830273589',
     'idstr': '4211012830273589', 'is_paid': False, 'reposts_count': 0, 'mblog_vip_type': 0,
     'in_reply_to_status_id': '', 'biz_feature': 0, 'more_info_type': 0, 'pic_urls': [], 'darwin_tags': [],
     'content_auth': 0, 'in_reply_to_user_id': '', 'source_type': 1, 'gif_ids': '',
     'created_at': 'Sat Feb 24 18:12:37 +0800 2018', 'text_tag_tips': [], 'textLength': 21, 'isLongText': False,
     'favorited': False, 'comments_count': 0, 'pending_approval_count': 0, 'positive_recom_flag': 0,
     'source': '<a href="http://app.weibo.com/t/feed/2W68oO" rel="nofollow">未通过审核应用</a>', 'mlevel': 0,
     'user': {'name': 'HiGDPU', 'avatar_large': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif',
              'followers_count': 13, 'allow_all_comment': True, 'ptype': 0, 'province': '100',
              'verified_source_url': '', 'idstr': '2203175032', 'mbrank': 0, 'domain': 'HiGDPU',
              'bi_followers_count': 0, 'credit_score': 80, 'story_read_state': -1, 'online_status': 0,
              'favourites_count': 5, 'star': 0, 'city': '1000', 'remark': '', 'mbtype': 0, 'verified_source': '',
              'block_app': 0, 'url': '', 'verified_reason_url': '', 'class': 1, 'verified': False, 'id': 2203175032,
              'profile_image_url': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_50.gif', 'urank': 6,
              'like': False, 'allow_all_act_msg': False, 'gender': 'm', 'location': '其他',
              'avatar_hd': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif', 'description': '',
              'weihao': '', 'screen_name': 'HiGDPU', 'follow_me': False, 'user_ability': 0, 'verified_trade': '',
              'vclub_member': 0, 'following': False, 'pagefriends_count': 0, 'block_word': 0, 'geo_enabled': True,
              'profile_url': 'HiGDPU', 'friends_count': 7, 'created_at': 'Wed Jun 29 11:20:30 +0800 2011',
              'lang': 'zh-cn', 'verified_type': -1, 'like_me': False, 'verified_reason': '',
              'insecurity': {'sexual_content': False}, 'statuses_count': 0}, 'in_reply_to_screen_name': ''},
    {'visible': {'type': 0, 'list_id': 0}, 'hasActionTypeCard': 0, 'userType': 0, 'id': 4210633019142532, 'geo': None,
     'comment_manage_info': {'approval_comment_type': 0, 'comment_manage_button': 1, 'comment_permission_type': 0},
     'text': 'HIacasa [胡巴宝宝睡了][胡巴目瞪口呆]1519376604.411698http://t.cn/RHM3DwB \u200b', 'source_allowclick': 0,
     'is_show_bulletin': 2, 'attitudes_count': 0, 'hot_weibo_tags': [], 'truncated': False, 'can_edit': False,
     'mid': '4210633019142532', 'idstr': '4210633019142532', 'is_paid': False, 'reposts_count': 0, 'mblog_vip_type': 0,
     'in_reply_to_status_id': '', 'biz_feature': 0, 'more_info_type': 0, 'pic_urls': [], 'darwin_tags': [],
     'content_auth': 0, 'in_reply_to_user_id': '', 'source_type': 1, 'gif_ids': '',
     'created_at': 'Fri Feb 23 17:03:24 +0800 2018', 'text_tag_tips': [], 'textLength': 72, 'isLongText': False,
     'favorited': False, 'comments_count': 0, 'pending_approval_count': 0, 'positive_recom_flag': 0,
     'source': '<a href="http://app.weibo.com/t/feed/2W68oO" rel="nofollow">未通过审核应用</a>', 'mlevel': 0,
     'user': {'name': 'HiGDPU', 'avatar_large': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif',
              'followers_count': 13, 'allow_all_comment': True, 'ptype': 0, 'province': '100',
              'verified_source_url': '', 'idstr': '2203175032', 'mbrank': 0, 'domain': 'HiGDPU',
              'bi_followers_count': 0, 'credit_score': 80, 'story_read_state': -1, 'online_status': 0,
              'favourites_count': 5, 'star': 0, 'city': '1000', 'remark': '', 'mbtype': 0, 'verified_source': '',
              'block_app': 0, 'url': '', 'verified_reason_url': '', 'class': 1, 'verified': False, 'id': 2203175032,
              'profile_image_url': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_50.gif', 'urank': 6,
              'like': False, 'allow_all_act_msg': False, 'gender': 'm', 'location': '其他',
              'avatar_hd': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif', 'description': '',
              'weihao': '', 'screen_name': 'HiGDPU', 'follow_me': False, 'user_ability': 0, 'verified_trade': '',
              'vclub_member': 0, 'following': False, 'pagefriends_count': 0, 'block_word': 0, 'geo_enabled': True,
              'profile_url': 'HiGDPU', 'friends_count': 7, 'created_at': 'Wed Jun 29 11:20:30 +0800 2011',
              'lang': 'zh-cn', 'verified_type': -1, 'like_me': False, 'verified_reason': '',
              'insecurity': {'sexual_content': False}, 'statuses_count': 0}, 'in_reply_to_screen_name': ''},
    {'visible': {'type': 0, 'list_id': 0}, 'hasActionTypeCard': 0, 'userType': 0, 'id': 4210596688076922, 'geo': None,
     'comment_manage_info': {'approval_comment_type': 0, 'comment_manage_button': 1, 'comment_permission_type': 0},
     'text': '微信 [胡巴宝宝睡了][胡巴目瞪口呆]1519367942.318144http://t.cn/RHM3DwB \u200b', 'source_allowclick': 0,
     'is_show_bulletin': 2, 'attitudes_count': 0, 'hot_weibo_tags': [], 'truncated': False, 'can_edit': False,
     'mid': '4210596688076922', 'idstr': '4210596688076922', 'is_paid': False, 'reposts_count': 0, 'mblog_vip_type': 0,
     'in_reply_to_status_id': '', 'biz_feature': 0, 'more_info_type': 0, 'pic_urls': [], 'darwin_tags': [],
     'content_auth': 0, 'in_reply_to_user_id': '', 'source_type': 1, 'gif_ids': '',
     'created_at': 'Fri Feb 23 14:39:02 +0800 2018', 'text_tag_tips': [], 'textLength': 69, 'isLongText': False,
     'favorited': False, 'comments_count': 0, 'pending_approval_count': 0, 'positive_recom_flag': 0,
     'source': '<a href="http://app.weibo.com/t/feed/2W68oO" rel="nofollow">未通过审核应用</a>', 'mlevel': 0,
     'user': {'name': 'HiGDPU', 'avatar_large': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif',
              'followers_count': 13, 'allow_all_comment': True, 'ptype': 0, 'province': '100',
              'verified_source_url': '', 'idstr': '2203175032', 'mbrank': 0, 'domain': 'HiGDPU',
              'bi_followers_count': 0, 'credit_score': 80, 'story_read_state': -1, 'online_status': 0,
              'favourites_count': 5, 'star': 0, 'city': '1000', 'remark': '', 'mbtype': 0, 'verified_source': '',
              'block_app': 0, 'url': '', 'verified_reason_url': '', 'class': 1, 'verified': False, 'id': 2203175032,
              'profile_image_url': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_50.gif', 'urank': 6,
              'like': False, 'allow_all_act_msg': False, 'gender': 'm', 'location': '其他',
              'avatar_hd': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif', 'description': '',
              'weihao': '', 'screen_name': 'HiGDPU', 'follow_me': False, 'user_ability': 0, 'verified_trade': '',
              'vclub_member': 0, 'following': False, 'pagefriends_count': 0, 'block_word': 0, 'geo_enabled': True,
              'profile_url': 'HiGDPU', 'friends_count': 7, 'created_at': 'Wed Jun 29 11:20:30 +0800 2011',
              'lang': 'zh-cn', 'verified_type': -1, 'like_me': False, 'verified_reason': '',
              'insecurity': {'sexual_content': False}, 'statuses_count': 0}, 'in_reply_to_screen_name': ''}],
     'previous_cursor': 0, 'interval': 0, 'marks': [], 'next_cursor': 0}

b = [{'text': 'test', 'floor_number': 1, 'idstr': '4211710300210914', 'disable_reply': 0, 'source_allowclick': 0,
      'source_type': 2, 'rootid': 4211710300210914, 'mid': '4211710300210914',
      'source': '<a href="http://weibo.com/" rel="nofollow">iPhone客户端</a>',
      'status': {'mlevel': 0, 'in_reply_to_user_id': '',
                 'comment_manage_info': {'comment_permission_type': -1, 'approval_comment_type': 0}, 'is_paid': False,
                 'pic_urls': [], 'is_show_bulletin': 2, 'source_allowclick': 0, 'in_reply_to_screen_name': '',
                 'text': 'Hihttp://t.cn/RHM3DwB', 'text_tag_tips': [], 'visible': {'type': 0, 'list_id': 0},
                 'pending_approval_count': 0, 'mid': '4211016852254679',
                 'source': '<a href="http://app.weibo.com/t/feed/2W68oO" rel="nofollow">未通过审核应用</a>',
                 'mblog_vip_type': 0, 'more_info_type': 0, 'positive_recom_flag': 0, 'favorited': False,
                 'user': {'avatar_hd': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif',
                          'like_me': False, 'statuses_count': 0, 'domain': 'HiGDPU', 'verified_trade': '',
                          'verified_type': -1, 'id': 2203175032, 'like': False, 'ptype': 0, 'favourites_count': 5,
                          'screen_name': 'HiGDPU', 'allow_all_act_msg': False, 'lang': 'zh-cn', 'vclub_member': 0,
                          'weihao': '', 'location': '其他', 'name': 'HiGDPU', 'urank': 6, 'province': '100',
                          'description': '', 'block_app': 0, 'gender': 'm', 'mbrank': 0, 'pagefriends_count': 0,
                          'verified_source': '', 'friends_count': 7, 'insecurity': {'sexual_content': False},
                          'mbtype': 0, 'class': 1, 'url': '', 'idstr': '2203175032', 'verified_reason': '',
                          'avatar_large': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_180.gif',
                          'online_status': 0, 'verified_source_url': '', 'geo_enabled': True, 'user_ability': 0,
                          'follow_me': False, 'star': 0, 'credit_score': 80, 'allow_all_comment': True, 'remark': '',
                          'story_read_state': -1, 'profile_url': 'HiGDPU', 'verified': False, 'following': False,
                          'followers_count': 13,
                          'profile_image_url': 'http://tvax1.sinaimg.cn/default/images/default_avatar_male_50.gif',
                          'block_word': 0, 'city': '1000', 'bi_followers_count': 0,
                          'created_at': 'Wed Jun 29 11:20:30 +0800 2011', 'verified_reason_url': ''}, 'userType': 0,
                 'reposts_count': 0, 'hasActionTypeCard': 0, 'content_auth': 0, 'idstr': '4211016852254679',
                 'attitudes_count': 0, 'isLongText': False, 'hot_weibo_tags': [], 'comments_count': 0, 'source_type': 1,
                 'created_at': 'Sat Feb 24 18:28:37 +0800 2018', 'can_edit': False, 'biz_feature': 0, 'darwin_tags': [],
                 'truncated': False, 'textLength': 21, 'geo': None, 'id': 4211016852254679, 'gif_ids': '',
                 'in_reply_to_status_id': ''}, 'id': 4211710300210914,
      'user': {'avatar_hd': 'http://tva3.sinaimg.cn/crop.216.238.1137.1137.1024/69824f94jw8etpiev8ng4j21kw1kwwob.jpg',
               'like_me': False, 'statuses_count': 62, 'domain': 'iamwc', 'verified_trade': '', 'verified_type': -1,
               'id': 1770147732, 'like': False, 'ptype': 0, 'favourites_count': 377, 'screen_name': 'wc菜花',
               'allow_all_act_msg': False, 'lang': 'zh-cn', 'vclub_member': 0, 'avatargj_id': 'gj_vip_011',
               'weihao': '', 'location': '广东 广州', 'name': 'wc菜花', 'urank': 29, 'province': '44', 'description': '你终于来了',
               'block_app': 0, 'gender': 'm', 'mbrank': 1, 'pagefriends_count': 0, 'verified_source': '',
               'friends_count': 248, 'insecurity': {'sexual_content': False}, 'mbtype': 2,
               'created_at': 'Thu Jul 15 14:18:16 +0800 2010', 'url': '', 'idstr': '1770147732', 'verified_reason': '',
               'avatar_large': 'http://tva3.sinaimg.cn/crop.216.238.1137.1137.180/69824f94jw8etpiev8ng4j21kw1kwwob.jpg',
               'online_status': 0, 'verified_source_url': '', 'geo_enabled': True, 'user_ability': 33555456,
               'follow_me': False, 'star': 0, 'cardid': 'star_286',
               'cover_image_phone': 'http://ww3.sinaimg.cn/crop.0.0.640.640.640/006qstmXjw1f4bygdospvj30ku0kuaa2.jpg',
               'credit_score': 80, 'allow_all_comment': True, 'remark': '', 'story_read_state': -1,
               'profile_url': 'iamwc', 'verified': False, 'following': False, 'followers_count': 291,
               'profile_image_url': 'http://tva3.sinaimg.cn/crop.216.238.1137.1137.50/69824f94jw8etpiev8ng4j21kw1kwwob.jpg',
               'block_word': 0, 'city': '1', 'bi_followers_count': 126, 'class': 1, 'verified_reason_url': ''},
      'created_at': 'Mon Feb 26 16:24:08 +0800 2018'}]

