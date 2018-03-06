# coding:utf-8
import re
import datetime
from html.parser import HTMLParser
from urllib.parse import urljoin
html = """
<!DOCTYPE HTML>
<html>
<head>
	<!DOCTYPE html>
<meta name=renderer content=webkit>
<meta charset="UTF-8">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN / DENY "> 
<title>广东药科大学</title>
<meta content="广东药科大学 广东药科大学官网 广药" name="description">
<meta content="广东药科大学 广东药科大学官网 广药" name="keywords">
<!--<meta name="viewport" content="width=device-width, initial-scale=1.0">-->
<meta name = "viewport" content = "width=device-width, minimum-scale=1, maximum-scale=1">
<meta name = "apple-mobile-web-app-capable" content = "yes" /> 
<link href="/Public/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
<link href="/Public/static/bootstrap/css/bootstrap.css" rel="stylesheet">
<link href="/Public/static/css/custom.css" rel="stylesheet">
<link href="/Public/Home/css/basic.css" rel="stylesheet">
<link href="/Public/Home/css/style_nc.css" rel="stylesheet">
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
<script src="css/bootstrap/js/html5shiv.min.js"></script>
<script src="css/bootstrap/js/respond.min.js"></script>
<script type="text/javascript" src="/Public/static/jquery-1.10.2.min.js"></script>
<![endif]-->
<!--[if gte IE 9]><!-->
<script type="text/javascript" src="/Public/static/jquery-2.0.3.min.js"></script>
<script type="text/javascript" src="/Public/static/bootstrap/js/bootstrap.min.js"></script>
<!--<![endif]-->

<!-- 页面header钩子，一般用于加载插件CSS文件和代码 -->

</head>
<body>
	<!-- 头部 -->
	<div class="header">
<div class="container"> 
<div class="logo">新闻网</div>
<div class="theme-popover">
<div class="theme-poptit">
<a href="javascript:;" title="关闭" class="close">×</a>
</div>
<div class="theme-popbod dform">
<img src="Public/Home/img/nc/weixin.jpg"  />   
</div>
</div>
<span> 
 <form class="search-form" action="" method="post">
<input type="text" value="" class="search" name="searchtext"/>  <!--/index.php?s=/home/newscenter/search.html-->
<a class="sch-btn" href="javascript:;" id="search" url="/index.php?s=/home/newscenter/search.html"> <i class="btn-search"></i></a>
</form>
</span>
<div class="ggicon"><span><a class="theme-login"  href="javascript:;" title="点击后打开大型二维码图片"><img src="/Public/Home/img/icon/weixin.png" /></a></span>
<span><a href=""><img src="/Public/Home/img/icon/weibo.png" /> </a></span>

</div>
</div>
</div>
<nav role="navigation" class="navbar navbar-inverse"> 
<!--navbar-fixed-top -->
	<div class="container navbarhead">	
        <div class="navbar-header">
          <button aria-controls="navbar" aria-expanded="false" data-target="#navbar" data-toggle="collapse" class="navbar-toggle" type="button">
            <span class="sr-only">切换导航</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
		<a class="navbar-brand" href="/index.php?s=/home/newscenter/index.html">首页</a>
        <div class="navbar-collapse collapse" id="navbar">			
          <ul class="nav navbar-nav">
				<li>
						<a href="/index.php?s=/home/newscenter/lists/category/yw.html">广药要闻</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/mt.html">媒体广药</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tz.html">广药图志</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sd.html">高教视点</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/fc.html">广药风采</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sz.html">理论时政</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/zl.html">专题专栏</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/xwzh.html">新闻纵横</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tgxz.html">投稿须知</a>
					</li>          </ul>             		  
        </div><!--/.nav-collapse -->
		</div>				
</nav>
<script>	
$(".btn-search").click(function(){	
	var url = $("#search").attr('url');
	var query  = $('.search-form').find('input').serialize();
	query = query.replace(/(&|^)(\w*?\d*?\-*?_*?)*?=?((?=&)|(?=$))/g,'');
	query = query.replace(/^&/g,'');
	if( url.indexOf('?')>0 ){
		url += '&' + query;
	}else{
		url += '?' + query;
	}
	window.location.href = url;
})
</script>
	<!-- /头部 -->
	
	<!-- 主体 -->
	
<div id="main-container" class="container">
    <div class="row">
	<div  style="height:20px;"></div>
     	
	<div class="col-sm-11 col-lg-9">			
	<section id="contents">	
	<div class="dhx"><a href="index.php">首页</a> 
	<a href="/index.php?s=/home/newscenter/lists.html">
		<i class="icon-chevron-right"></i> 	</a> >	<a href="/index.php?s=/home/newscenter/lists/category/newcenter.html">
		<i class="icon-chevron-right"></i> 新闻中心	</a> ><span><a href="/index.php?s=/home/newscenter/lists/category/fc.html">
		<i class="icon-chevron-right"></i>广药风采	</a></span>		
	<span> > <a href="/index.php?s=/home/article/lists/category/fc.html">我校学子在第三届中国“互联网+” “建行杯”广东省分赛决赛中获铜奖 </a></span>
	</div> 
	<div class="title text-center">	
		<h3>我校学子在第三届中国“互联网+” “建行杯”广东省分赛决赛中获铜奖</h3>		
		<small>发布时间：2017-08-11 来源：信工学院|0 点击量：865</small>
	</div>	
		<hr/>	
		<div class="content">
		<img alt="" src="http://www.gdpu.edu.cn/gdpunews/uploadfile/2017/0811/20170811053627849.jpg" style="width: 600px; height: 450px;" /><br />
<br />
<span style="font-size:18px;"><span style="font-family:楷体_gb2312;">　　8月4日，第三届中国&ldquo;互联网+&rdquo;大学生创新创业大赛&ldquo;建行杯&rdquo;广东省分赛在广东工业大学圆满落幕。我校医药信息工程学院&quot;衡必康团队&quot;进入了本次省级分赛的决赛，并以&quot;梳康协同服务&quot;项目获大赛初创组铜奖。&nbsp;<br />
　　为做好此次参赛的准备工作，我校自2016年起举办以&ldquo;拥抱&lsquo;互联网+&rsquo;和&lsquo;大健康&rsquo;时代共筑创新创业梦想&rdquo;为主题的&ldquo;互联网+大健康&rdquo;创新创业大赛，从中选拔出6支队伍参加第三届中国&ldquo;互联网+&rdquo;大学生创新创业大赛，其中，&ldquo;衡必康团队&rdquo;进入了本次省级分赛的决赛。&nbsp;<br />
　　赛前，经过数月的培训，&ldquo;衡必康团队&rdquo;对宏观环境分析、市场需求分析、竞争态势分析、产品策略分析、运营策略分析、人力资源分析、投入产出分析和风险分析等进行了深入讨论和调查研究。在省分赛决赛现场，选手们对项目从产品服务介绍、市场分析及定位、商业模式、营销策略、财务分析、风险控制、团队等方面进行了充分展示，受到评委们的充分肯定，并最终获得铜奖。</span></span><br />
<br />
&nbsp;<img alt="" src="http://www.gdpu.edu.cn/gdpunews/uploadfile/2017/0811/20170811053644429.jpg" style="width: 600px; height: 444px;" /><br />
<br />
<span style="font-size:18px;"><span style="font-family:楷体_gb2312;">　　此次参赛，同学们得到了向其他更加优秀团队学习的机会及专家教授们的指导，也为我校今后进一步深化创新创业教育改革、提高人才培养质量积累了宝贵的经验。&nbsp;<br />
　　据悉，本届大赛主题是&ldquo;搏击&lsquo;互联网+&rsquo;新时代，壮大创新创业生力军&rdquo;。大赛旨在深化高等教育综合改革，激发大学生的创造力，培养造就&ldquo;大众创业、万众创新&rdquo;的生力军；推动赛事成果转化和产学研用紧密结合，促进&ldquo;互联网+&rdquo;新业态形成，服务经济提质增效升级；以创新引领创业、以创业带动就业，推动高校毕业生更高质量创业就业。&nbsp;<br />
　　按照省分赛规程和高校推荐，共有来自119所高校的1276个项目入围省复赛。根据省内外专家评委的网评结果，共有来自34所高校的80个项目晋级省决赛，其中，创意组33个，初创组20个，成长组7个，就业型创业组20个。 最终决出本届省赛的金奖12名，银奖24名，铜奖44名。</span></span><br />
		</div>
		<div  style="height:20px;"></div>
		<hr/>
		<div class="pull col-sm-11 col-lg-9">
			<span class="pull-left">
								<p><span>下一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/5801.html">我校外国语学院学子获全国大学生写作大赛特等奖</a></p>			</span>
		</div>
		<div class="clearer"></div>
		</section>
		
	</div>	

	 
<div class="col-sm-11 col-lg-3">
	<div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">24小时排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（2）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">一周排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（738）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6691.html" title="【南方＋】广药医学生见义勇为救路人，事后他竟然说很惭愧...... 阅读（206）">【南方＋】广药医学生见义...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6699.html" title="学校召开校园安全工作会议 阅读（196）">学校召开校园安全工作会议</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6700.html" title="不忘初心，坚定信念，为培育英才努力奋斗——医药化工学院召开第二届教职工代表大会暨工会会员代表大会 阅读（129）">不忘初心，坚定信念，为培...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/2530.html" title="校长/党委副书记  郭  姣 阅读（40）">校长/党委副书记  郭 ...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（2）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">本月排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6676.html" title="广东药科大学2018年公开招聘人员公告 阅读（15906）">广东药科大学2018年公...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6690.html" title="学校举行2018年离退休老同志迎春茶话会 阅读（829）">学校举行2018年离退休...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（738）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6688.html" title="全国高校健康服务与管理专业 “十三五”规划系列教材评审委员会一届一次会议在海口召开 阅读（651）">全国高校健康服务与管理专...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6686.html" title="我校校长郭姣教授应邀参加中俄医科大学联盟医院揭牌仪式暨一带一路中俄医科大学联盟医学与健康学术会议并发表主旨演讲 阅读（629）">我校校长郭姣教授应邀参加...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6687.html" title="我校与深圳市人才集团有限公司签订《战略合作框架协议》 阅读（618）">我校与深圳市人才集团有限...</a></li>	 
		</div>
	  </div>
	</div>
       
    </div>
</div>

<script type="text/javascript">
    $(function(){
        $(window).resize(function(){
            $("#main-container").css("min-height", $(window).height() - 230);
        }).resize();
    })
</script>
	<!-- /主体 -->

	<!-- 底部 -->
	<div class="footer">
<div class="container">
广东药科大学党委宣传部 版权所有 Copyright © 2017  制作单位：现代教育技术中心网络部  v1.0
</div>
<script type="text/javascript">
(function(){
	var ThinkPHP = window.Think = {
		"ROOT"   : "", //当前网站地址
		"APP"    : "/index.php?s=", //当前项目地址
		"PUBLIC" : "/Public", //项目公共目录地址
		"DEEP"   : "/", //PATHINFO分割符
		"MODEL"  : ["3", "1", "html"],
		"VAR"    : ["m", "c", "a"]
	}
})();
</script>

 <!-- 用于加载js代码 -->
<!-- 页面footer钩子，一般用于加载插件JS文件和JS代码 -->
<div class="hidden"><!-- 用于加载统计代码等隐藏元素 -->
	
</div>
<script>
$(document).ready(function() {
	$('.theme-login').click(function(){
		$('.theme-popover-mask').fadeIn(100);
		$('.theme-popover').slideDown(200);
		})
		$('.theme-poptit .close').click(function(){
		$('.theme-popover-mask').fadeOut(100);
		$('.theme-popover').slideUp(200);
	})
});
</script>
	<!-- /底部 -->
</body>
</html>"""

html1 = """
<!DOCTYPE HTML>
<html>
<head>
	<!DOCTYPE html>
<meta name=renderer content=webkit>
<meta charset="UTF-8">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN / DENY "> 
<title>广东药科大学</title>
<meta content="广东药科大学 广东药科大学官网 广药" name="description">
<meta content="广东药科大学 广东药科大学官网 广药" name="keywords">
<!--<meta name="viewport" content="width=device-width, initial-scale=1.0">-->
<meta name = "viewport" content = "width=device-width, minimum-scale=1, maximum-scale=1">
<meta name = "apple-mobile-web-app-capable" content = "yes" /> 
<link href="/Public/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
<link href="/Public/static/bootstrap/css/bootstrap.css" rel="stylesheet">
<link href="/Public/static/css/custom.css" rel="stylesheet">
<link href="/Public/Home/css/basic.css" rel="stylesheet">
<link href="/Public/Home/css/style_nc.css" rel="stylesheet">
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
<script src="css/bootstrap/js/html5shiv.min.js"></script>
<script src="css/bootstrap/js/respond.min.js"></script>
<script type="text/javascript" src="/Public/static/jquery-1.10.2.min.js"></script>
<![endif]-->
<!--[if gte IE 9]><!-->
<script type="text/javascript" src="/Public/static/jquery-2.0.3.min.js"></script>
<script type="text/javascript" src="/Public/static/bootstrap/js/bootstrap.min.js"></script>
<!--<![endif]-->

<!-- 页面header钩子，一般用于加载插件CSS文件和代码 -->

</head>
<body>
	<!-- 头部 -->
	<div class="header">
<div class="container"> 
<div class="logo">新闻网</div>
<div class="theme-popover">
<div class="theme-poptit">
<a href="javascript:;" title="关闭" class="close">×</a>
</div>
<div class="theme-popbod dform">
<img src="Public/Home/img/nc/weixin.jpg"  />   
</div>
</div>
<span> 
 <form class="search-form" action="" method="post">
<input type="text" value="" class="search" name="searchtext"/>  <!--/index.php?s=/home/newscenter/search.html-->
<a class="sch-btn" href="javascript:;" id="search" url="/index.php?s=/home/newscenter/search.html"> <i class="btn-search"></i></a>
</form>
</span>
<div class="ggicon"><span><a class="theme-login"  href="javascript:;" title="点击后打开大型二维码图片"><img src="/Public/Home/img/icon/weixin.png" /></a></span>
<span><a href=""><img src="/Public/Home/img/icon/weibo.png" /> </a></span>

</div>
</div>
</div>
<nav role="navigation" class="navbar navbar-inverse"> 
<!--navbar-fixed-top -->
	<div class="container navbarhead">	
        <div class="navbar-header">
          <button aria-controls="navbar" aria-expanded="false" data-target="#navbar" data-toggle="collapse" class="navbar-toggle" type="button">
            <span class="sr-only">切换导航</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
		<a class="navbar-brand" href="/index.php?s=/home/newscenter/index.html">首页</a>
        <div class="navbar-collapse collapse" id="navbar">			
          <ul class="nav navbar-nav">
				<li>
						<a href="/index.php?s=/home/newscenter/lists/category/yw.html">广药要闻</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/mt.html">媒体广药</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tz.html">广药图志</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sd.html">高教视点</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/fc.html">广药风采</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sz.html">理论时政</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/zl.html">专题专栏</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/xwzh.html">新闻纵横</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tgxz.html">投稿须知</a>
					</li>          </ul>             		  
        </div><!--/.nav-collapse -->
		</div>				
</nav>
<script>	
$(".btn-search").click(function(){	
	var url = $("#search").attr('url');
	var query  = $('.search-form').find('input').serialize();
	query = query.replace(/(&|^)(\w*?\d*?\-*?_*?)*?=?((?=&)|(?=$))/g,'');
	query = query.replace(/^&/g,'');
	if( url.indexOf('?')>0 ){
		url += '&' + query;
	}else{
		url += '?' + query;
	}
	window.location.href = url;
})
</script>
	<!-- /头部 -->
	
	<!-- 主体 -->
	
<div id="main-container" class="container">
    <div class="row">
	<div  style="height:20px;"></div>
     	
	<div class="col-sm-11 col-lg-9">			
	<section id="contents">	
	<div class="dhx"><a href="index.php">首页</a> 
	<a href="/index.php?s=/home/newscenter/lists.html">
		<i class="icon-chevron-right"></i> 	</a> >	<a href="/index.php?s=/home/newscenter/lists/category/newcenter.html">
		<i class="icon-chevron-right"></i> 新闻中心	</a> ><span><a href="/index.php?s=/home/newscenter/lists/category/yw.html">
		<i class="icon-chevron-right"></i>广药要闻	</a></span>		
	<span> > <a href="/index.php?s=/home/article/lists/category/yw.html">我校广东省医药3D打印机及个性化医疗工程技术研究中心举行授牌仪式 </a></span>
	</div> 
	<div class="title text-center">	
		<h3>我校广东省医药3D打印机及个性化医疗工程技术研究中心举行授牌仪式</h3>		
		<small>发布时间：2018-01-31 来源：医药信息工程学院 点击量：960</small>
	</div>	
		<hr/>	
		<div class="content">
		<p align="center">
	<span style="font-family:KaiTi_GB2312;font-size:18px;"><img src="/Uploads/Editor/2018-01-31/5a7174f298c12.JPG" alt="" /><br />
</span>
</p>
<p align="center">
	<span style="font-family:KaiTi_GB2312;font-size:18px;"><br />
</span> 
</p>
<p>
	<span style="font-family:KaiTi_GB2312;font-size:18px;">　　1月26日，我校广东省医药3D打印机及个性化医疗工程技术研究中心（以下简称工程中心）在深圳森工科技有限公司（以下简称森工科技）授牌。我校党委副书记巫宏星、医药信息工程学院党委书记邓钜新、党委副书记郭超龙、学校毕业生就业指导中心副主任邱群光、森工科技总经理杨海、副总经理罗建旭等参加了授牌仪式。该工程中心是由我校医药信息工程学院牵头，联合森工科技、深圳邦普医疗设备系统有限公司联合申报并获得广东省科技厅认定的省级工程技术研究中心。</span> 
</p>
<span style="font-family:KaiTi_GB2312;font-size:18px;">　　授牌仪式开始前，首先由森工科技负责人介绍了企业创新创业历程、产品研发、工程中心产学研合作、欧美市场开发等方面的情况。随后，我校医药信息工程学院生物医学工程系副主任、工程中心冯博华博士对3D打印技术面临的机遇和挑战、个性化医疗与生物医学工程研发热点及工程中心下一步工作要点进行了汇报。</span><br />
<span style="font-family:KaiTi_GB2312;font-size:18px;">　　巫宏星表示，森工科技与我校医药信息工程学院，尤其是生物医学工程系在人才培养、科技合作、实践基地建设等方面有着长期良好的合作。此次由我校牵头，联合包括森工科技在内的高新技术企业参与，成功认定了省级工程技术研究中心，是校企各方努力的成果，对医药信息工程学院，尤其是生物医学工程专业的发展将提供重要的平台支撑。在我校建设高水平大学和申报博士学位授予权等新任务、新形势要求下，希望信工学院携手森工科技，切实推进工程中心的建设，合力将平台做大做强，发挥平台的产学研协同作用和人才集聚优势，聚焦个性化医学应用需求，注重科研成果的产业化，充分发挥高校的智力支撑作用和企业的智能制造优势，使校企合作真正“开花结果”，并使工程中心的建设模式为学校其他专业发展提供示范。</span><br />
<span style="font-family:KaiTi_GB2312;font-size:18px;">　　对于森工科技当年的初创团队“四人组”、我校2011届生物医学工程专业毕业生杨海、罗建旭、郑加华和方映斌校友，巫宏星表示，看到学生创业成功感到非常欣慰，希望他们的创新、创业事迹，能为师弟师妹们传递满满的正能量。同时巫宏星还勉励他们继续发扬“自强不息、追求卓越”的广药大精神，在工程中心建设和企业各方面工作中始终坚韧不拔，持续奋斗，科学发展，赢得先机。</span><br />
<span style="font-family:KaiTi_GB2312;font-size:18px;">　　授牌仪式后，巫宏星一行考察了森工科技的试验室，研发部门、装配车间、市场运营部门，详细了解了3D打印机从设计研发到产品制造、运营、医学应用的情况，并慰问了正在企业进行实习、毕业设计的学生代表和企业在职的校友代表。</span><br />
<span style="font-family:KaiTi_GB2312;font-size:18px;">　　据悉，森工科技系于2012年成立的国家高新技术企业，拥有完善的ISO9001质量管理体系认证的3D打印机制造商，秉承“3D打印改变生活”为其核心价值，其拳头产品MakerPi创意派系列工业3D打印机广受国内外包括日本、澳大利亚、英国、德国等国家专业客户的青睐，其中拥有首发自主知识产权的混色3D打印机在2016年的全国双创周深圳主会场上更是受到广泛关注。</span>		</div>
		<div  style="height:20px;"></div>
		<hr/>
		<div class="pull col-sm-11 col-lg-9">
			<span class="pull-left">
				<p><span>上一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6679.html">我校罗祥智老师获“广东省研究生德育工作先进个人”表彰</a></p>				<p><span>下一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6684.html">我校召开第七届教职工代表大会暨第九届工会会员代表大会特别会议</a></p>			</span>
		</div>
		<div class="clearer"></div>
		</section>
		
	</div>	

	 
<div class="col-sm-11 col-lg-3">
	<div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">24小时排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6700.html" title="不忘初心，坚定信念，为培育英才努力奋斗——医药化工学院召开第二届教职工代表大会暨工会会员代表大会 阅读（193）">不忘初心，坚定信念，为培...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">一周排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（767）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6699.html" title="学校召开校园安全工作会议 阅读（299）">学校召开校园安全工作会议</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6691.html" title="【南方＋】广药医学生见义勇为救路人，事后他竟然说很惭愧...... 阅读（247）">【南方＋】广药医学生见义...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6700.html" title="不忘初心，坚定信念，为培育英才努力奋斗——医药化工学院召开第二届教职工代表大会暨工会会员代表大会 阅读（193）">不忘初心，坚定信念，为培...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/2530.html" title="校长/党委副书记  郭  姣 阅读（46）">校长/党委副书记  郭 ...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（8）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">本月排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6676.html" title="广东药科大学2018年公开招聘人员公告 阅读（16203）">广东药科大学2018年公...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6690.html" title="学校举行2018年离退休老同志迎春茶话会 阅读（864）">学校举行2018年离退休...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（767）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6688.html" title="全国高校健康服务与管理专业 “十三五”规划系列教材评审委员会一届一次会议在海口召开 阅读（675）">全国高校健康服务与管理专...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6686.html" title="我校校长郭姣教授应邀参加中俄医科大学联盟医院揭牌仪式暨一带一路中俄医科大学联盟医学与健康学术会议并发表主旨演讲 阅读（651）">我校校长郭姣教授应邀参加...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6687.html" title="我校与深圳市人才集团有限公司签订《战略合作框架协议》 阅读（645）">我校与深圳市人才集团有限...</a></li>	 
		</div>
	  </div>
	</div>
       
    </div>
</div>

<script type="text/javascript">
    $(function(){
        $(window).resize(function(){
            $("#main-container").css("min-height", $(window).height() - 230);
        }).resize();
    })
</script>
	<!-- /主体 -->

	<!-- 底部 -->
	<div class="footer">
<div class="container">
广东药科大学党委宣传部 版权所有 Copyright © 2017  制作单位：现代教育技术中心网络部  v1.0
</div>
<script type="text/javascript">
(function(){
	var ThinkPHP = window.Think = {
		"ROOT"   : "", //当前网站地址
		"APP"    : "/index.php?s=", //当前项目地址
		"PUBLIC" : "/Public", //项目公共目录地址
		"DEEP"   : "/", //PATHINFO分割符
		"MODEL"  : ["3", "1", "html"],
		"VAR"    : ["m", "c", "a"]
	}
})();
</script>

 <!-- 用于加载js代码 -->
<!-- 页面footer钩子，一般用于加载插件JS文件和JS代码 -->
<div class="hidden"><!-- 用于加载统计代码等隐藏元素 -->
	
</div>
<script>
$(document).ready(function() {
	$('.theme-login').click(function(){
		$('.theme-popover-mask').fadeIn(100);
		$('.theme-popover').slideDown(200);
		})
		$('.theme-poptit .close').click(function(){
		$('.theme-popover-mask').fadeOut(100);
		$('.theme-popover').slideUp(200);
	})
});
</script>
	<!-- /底部 -->
</body>
</html>"""

html2 = """
<!DOCTYPE HTML>
<html>
<head>
	<!DOCTYPE html>
<meta name=renderer content=webkit>
<meta charset="UTF-8">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN / DENY "> 
<title>广东药科大学</title>
<meta content="广东药科大学 广东药科大学官网 广药" name="description">
<meta content="广东药科大学 广东药科大学官网 广药" name="keywords">
<!--<meta name="viewport" content="width=device-width, initial-scale=1.0">-->
<meta name = "viewport" content = "width=device-width, minimum-scale=1, maximum-scale=1">
<meta name = "apple-mobile-web-app-capable" content = "yes" /> 
<link href="/Public/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
<link href="/Public/static/bootstrap/css/bootstrap.css" rel="stylesheet">
<link href="/Public/static/css/custom.css" rel="stylesheet">
<link href="/Public/Home/css/basic.css" rel="stylesheet">
<link href="/Public/Home/css/style_nc.css" rel="stylesheet">
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
<script src="css/bootstrap/js/html5shiv.min.js"></script>
<script src="css/bootstrap/js/respond.min.js"></script>
<script type="text/javascript" src="/Public/static/jquery-1.10.2.min.js"></script>
<![endif]-->
<!--[if gte IE 9]><!-->
<script type="text/javascript" src="/Public/static/jquery-2.0.3.min.js"></script>
<script type="text/javascript" src="/Public/static/bootstrap/js/bootstrap.min.js"></script>
<!--<![endif]-->

<!-- 页面header钩子，一般用于加载插件CSS文件和代码 -->

</head>
<body>
	<!-- 头部 -->
	<div class="header">
<div class="container"> 
<div class="logo">新闻网</div>
<div class="theme-popover">
<div class="theme-poptit">
<a href="javascript:;" title="关闭" class="close">×</a>
</div>
<div class="theme-popbod dform">
<img src="Public/Home/img/nc/weixin.jpg"  />   
</div>
</div>
<span> 
 <form class="search-form" action="" method="post">
<input type="text" value="" class="search" name="searchtext"/>  <!--/index.php?s=/home/newscenter/search.html-->
<a class="sch-btn" href="javascript:;" id="search" url="/index.php?s=/home/newscenter/search.html"> <i class="btn-search"></i></a>
</form>
</span>
<div class="ggicon"><span><a class="theme-login"  href="javascript:;" title="点击后打开大型二维码图片"><img src="/Public/Home/img/icon/weixin.png" /></a></span>
<span><a href=""><img src="/Public/Home/img/icon/weibo.png" /> </a></span>

</div>
</div>
</div>
<nav role="navigation" class="navbar navbar-inverse"> 
<!--navbar-fixed-top -->
	<div class="container navbarhead">	
        <div class="navbar-header">
          <button aria-controls="navbar" aria-expanded="false" data-target="#navbar" data-toggle="collapse" class="navbar-toggle" type="button">
            <span class="sr-only">切换导航</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
		<a class="navbar-brand" href="/index.php?s=/home/newscenter/index.html">首页</a>
        <div class="navbar-collapse collapse" id="navbar">			
          <ul class="nav navbar-nav">
				<li>
						<a href="/index.php?s=/home/newscenter/lists/category/yw.html">广药要闻</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/mt.html">媒体广药</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tz.html">广药图志</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sd.html">高教视点</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/fc.html">广药风采</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sz.html">理论时政</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/zl.html">专题专栏</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/xwzh.html">新闻纵横</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tgxz.html">投稿须知</a>
					</li>          </ul>             		  
        </div><!--/.nav-collapse -->
		</div>				
</nav>
<script>	
$(".btn-search").click(function(){	
	var url = $("#search").attr('url');
	var query  = $('.search-form').find('input').serialize();
	query = query.replace(/(&|^)(\w*?\d*?\-*?_*?)*?=?((?=&)|(?=$))/g,'');
	query = query.replace(/^&/g,'');
	if( url.indexOf('?')>0 ){
		url += '&' + query;
	}else{
		url += '?' + query;
	}
	window.location.href = url;
})
</script>
	<!-- /头部 -->
	
	<!-- 主体 -->
	
<div id="main-container" class="container">
    <div class="row">
	<div  style="height:20px;"></div>
     	
	<div class="col-sm-11 col-lg-9">			
	<section id="contents">	
	<div class="dhx"><a href="index.php">首页</a> 
	<a href="/index.php?s=/home/newscenter/lists.html">
		<i class="icon-chevron-right"></i> 	</a> >	<a href="/index.php?s=/home/newscenter/lists/category/newcenter.html">
		<i class="icon-chevron-right"></i> 新闻中心	</a> ><span><a href="/index.php?s=/home/newscenter/lists/category/yw.html">
		<i class="icon-chevron-right"></i>广药要闻	</a></span>		
	<span> > <a href="/index.php?s=/home/article/lists/category/yw.html">学校举行2018年离退休老同志迎春茶话会 </a></span>
	</div> 
	<div class="title text-center">	
		<h3>学校举行2018年离退休老同志迎春茶话会</h3>		
		<small>发布时间：2018-02-07 来源：离休办，退休办，党政办 点击量：830</small>
	</div>	
		<hr/>	
		<div class="content">
		<p class="1" align="center" style="text-align:left;">
	<span style="font-family:KaiTi_GB2312;font-size:18px;line-height:1.5;"> &nbsp; &nbsp;&nbsp;2月7日，学校在宝岗校区离退休教职工活动中心举行2018年离退休老同志迎春茶话会。学校党委书记杨海涛、校长郭姣、党委副书记巫宏星、副校长张陆勇出席茶话会，为离退休老同志们送上新春祝福和诚挚问候。全体离休干部、退休厅级老领导以及退休教职工党委委员、关心下一代工作委员会和老教育工作者协会负责同志出席了会议。 &nbsp; &nbsp; &nbsp;&nbsp;</span>
</p>
<p class="1" style="text-indent:28.0pt;">
	<span style="font-family:KaiTi_GB2312;font-size:18px;">会上，首先由巫宏星向离退休老同志通报了2017年度学校发展建设情况。过去一年里，学校取得的成绩，特别是临床医学学科进入ESI全球前1%、药学学科在全国第四轮学科评估中位列全国并列第21名、省市共建及云浮校区顺利推进、科研经费总量翻番、国家基金立项数倍增、荣获“全国创新争先奖状”及“何梁何利基金奖”、“珠江学者”项目再次突破并入选2名特聘教授等发展成就让老同志们备感振奋。</span>
</p>
<p class="1" style="text-indent:31.65pt;">
	<span style="font-family:KaiTi_GB2312;font-size:18px;">随后，郭姣作了讲话。她指出，学校坚持贯彻落实党的十八大、十九大精神以及国家和广东省“双一流”大学建设的思路和部署，坚持不懈地进行高水平药科大学建设，尤其在办学格局、学科建设、人才引进等方面取得了可喜成绩。针对离退休老同志普遍关心的宝岗校区资产管理方面存在的问题，郭姣也通报了学校的初步方案，并要求相关部门一定要加快工作步伐，也希望充分发挥离退休老同志智慧和心力，全校拧成一股绳，尽快予以解决。&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
</p>
<p class="1" style="text-indent:28.0pt;">
	<span style="font-family:KaiTi_GB2312;font-size:18px;">会上，离退休老同志们踊跃发言，纷纷对学校党政领导的亲切慰问表示衷心感谢，对学校一年来所取得的发展成就以及学校领导班子的工作给予了高度评价，同时对学校2018年的工作提出了有建设性的意见和建议。</span>
</p>
<p class="1" style="text-indent:7.0pt;">
	<span style="font-family:KaiTi_GB2312;font-size:18px;">　&nbsp;&nbsp;杨海涛作了总结讲话。杨海涛表示，非常感谢离退休老同志对学校的关心、包容、支持，认为学校发展到今天的规模和层次是广药大几代人努力奋斗的结果，学校不会忘记老同志们所做的贡献，学校的发展成果也将由包括老同志在内的全校教职工分享，2018年，学校将努力让更多的老同志感受到学校的快速发展。最后，杨海涛表示，对于宝岗校区资产管理方面存在的问题，学校将全力配合上级相关部门，运用法律手段确保校区资源得到有效保护和利用。</span>
</p>
<p class="1" style="text-indent:28.0pt;">
	<span style="font-family:KaiTi_GB2312;font-size:18px;">党政办、党委组织部、人事处、离休办、退休办、宝岗校区办的有关同志出席了会议。</span>
</p>
<p class="MsoNormal">
	<span style="font-family:KaiTi_GB2312;font-size:18px;">&nbsp;</span>
</p>		</div>
		<div  style="height:20px;"></div>
		<hr/>
		<div class="pull col-sm-11 col-lg-9">
			<span class="pull-left">
				<p><span>上一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6689.html">郭姣校长慰问海南校友</a></p>				<p><span>下一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6699.html">学校召开校园安全工作会议</a></p>			</span>
		</div>
		<div class="clearer"></div>
		</section>
		
	</div>	

	 
<div class="col-sm-11 col-lg-3">
	<div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">24小时排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（3）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">一周排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（739）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6691.html" title="【南方＋】广药医学生见义勇为救路人，事后他竟然说很惭愧...... 阅读（207）">【南方＋】广药医学生见义...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6699.html" title="学校召开校园安全工作会议 阅读（200）">学校召开校园安全工作会议</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6700.html" title="不忘初心，坚定信念，为培育英才努力奋斗——医药化工学院召开第二届教职工代表大会暨工会会员代表大会 阅读（131）">不忘初心，坚定信念，为培...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/2530.html" title="校长/党委副书记  郭  姣 阅读（40）">校长/党委副书记  郭 ...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（3）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">本月排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6676.html" title="广东药科大学2018年公开招聘人员公告 阅读（15915）">广东药科大学2018年公...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6690.html" title="学校举行2018年离退休老同志迎春茶话会 阅读（831）">学校举行2018年离退休...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（739）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6688.html" title="全国高校健康服务与管理专业 “十三五”规划系列教材评审委员会一届一次会议在海口召开 阅读（651）">全国高校健康服务与管理专...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6686.html" title="我校校长郭姣教授应邀参加中俄医科大学联盟医院揭牌仪式暨一带一路中俄医科大学联盟医学与健康学术会议并发表主旨演讲 阅读（629）">我校校长郭姣教授应邀参加...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6687.html" title="我校与深圳市人才集团有限公司签订《战略合作框架协议》 阅读（620）">我校与深圳市人才集团有限...</a></li>	 
		</div>
	  </div>
	</div>
       
    </div>
</div>

<script type="text/javascript">
    $(function(){
        $(window).resize(function(){
            $("#main-container").css("min-height", $(window).height() - 230);
        }).resize();
    })
</script>
	<!-- /主体 -->

	<!-- 底部 -->
	<div class="footer">
<div class="container">
广东药科大学党委宣传部 版权所有 Copyright © 2017  制作单位：现代教育技术中心网络部  v1.0
</div>
<script type="text/javascript">
(function(){
	var ThinkPHP = window.Think = {
		"ROOT"   : "", //当前网站地址
		"APP"    : "/index.php?s=", //当前项目地址
		"PUBLIC" : "/Public", //项目公共目录地址
		"DEEP"   : "/", //PATHINFO分割符
		"MODEL"  : ["3", "1", "html"],
		"VAR"    : ["m", "c", "a"]
	}
})();
</script>

 <!-- 用于加载js代码 -->
<!-- 页面footer钩子，一般用于加载插件JS文件和JS代码 -->
<div class="hidden"><!-- 用于加载统计代码等隐藏元素 -->
	
</div>
<script>
$(document).ready(function() {
	$('.theme-login').click(function(){
		$('.theme-popover-mask').fadeIn(100);
		$('.theme-popover').slideDown(200);
		})
		$('.theme-poptit .close').click(function(){
		$('.theme-popover-mask').fadeOut(100);
		$('.theme-popover').slideUp(200);
	})
});
</script>
	<!-- /底部 -->
</body>
</html>"""

html3 = """
<!DOCTYPE HTML>
<html>
<head>
	<!DOCTYPE html>
<meta name=renderer content=webkit>
<meta charset="UTF-8">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN / DENY "> 
<title>广东药科大学</title>
<meta content="广东药科大学 广东药科大学官网 广药" name="description">
<meta content="广东药科大学 广东药科大学官网 广药" name="keywords">
<!--<meta name="viewport" content="width=device-width, initial-scale=1.0">-->
<meta name = "viewport" content = "width=device-width, minimum-scale=1, maximum-scale=1">
<meta name = "apple-mobile-web-app-capable" content = "yes" /> 
<link href="/Public/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
<link href="/Public/static/bootstrap/css/bootstrap.css" rel="stylesheet">
<link href="/Public/static/css/custom.css" rel="stylesheet">
<link href="/Public/Home/css/basic.css" rel="stylesheet">
<link href="/Public/Home/css/style_nc.css" rel="stylesheet">
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
<script src="css/bootstrap/js/html5shiv.min.js"></script>
<script src="css/bootstrap/js/respond.min.js"></script>
<script type="text/javascript" src="/Public/static/jquery-1.10.2.min.js"></script>
<![endif]-->
<!--[if gte IE 9]><!-->
<script type="text/javascript" src="/Public/static/jquery-2.0.3.min.js"></script>
<script type="text/javascript" src="/Public/static/bootstrap/js/bootstrap.min.js"></script>
<!--<![endif]-->

<!-- 页面header钩子，一般用于加载插件CSS文件和代码 -->

</head>
<body>
	<!-- 头部 -->
	<div class="header">
<div class="container"> 
<div class="logo">新闻网</div>
<div class="theme-popover">
<div class="theme-poptit">
<a href="javascript:;" title="关闭" class="close">×</a>
</div>
<div class="theme-popbod dform">
<img src="Public/Home/img/nc/weixin.jpg"  />   
</div>
</div>
<span> 
 <form class="search-form" action="" method="post">
<input type="text" value="" class="search" name="searchtext"/>  <!--/index.php?s=/home/newscenter/search.html-->
<a class="sch-btn" href="javascript:;" id="search" url="/index.php?s=/home/newscenter/search.html"> <i class="btn-search"></i></a>
</form>
</span>
<div class="ggicon"><span><a class="theme-login"  href="javascript:;" title="点击后打开大型二维码图片"><img src="/Public/Home/img/icon/weixin.png" /></a></span>
<span><a href=""><img src="/Public/Home/img/icon/weibo.png" /> </a></span>

</div>
</div>
</div>
<nav role="navigation" class="navbar navbar-inverse"> 
<!--navbar-fixed-top -->
	<div class="container navbarhead">	
        <div class="navbar-header">
          <button aria-controls="navbar" aria-expanded="false" data-target="#navbar" data-toggle="collapse" class="navbar-toggle" type="button">
            <span class="sr-only">切换导航</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
		<a class="navbar-brand" href="/index.php?s=/home/newscenter/index.html">首页</a>
        <div class="navbar-collapse collapse" id="navbar">			
          <ul class="nav navbar-nav">
				<li>
						<a href="/index.php?s=/home/newscenter/lists/category/yw.html">广药要闻</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/mt.html">媒体广药</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tz.html">广药图志</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sd.html">高教视点</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/fc.html">广药风采</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sz.html">理论时政</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/zl.html">专题专栏</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/xwzh.html">新闻纵横</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tgxz.html">投稿须知</a>
					</li>          </ul>             		  
        </div><!--/.nav-collapse -->
		</div>				
</nav>
<script>	
$(".btn-search").click(function(){	
	var url = $("#search").attr('url');
	var query  = $('.search-form').find('input').serialize();
	query = query.replace(/(&|^)(\w*?\d*?\-*?_*?)*?=?((?=&)|(?=$))/g,'');
	query = query.replace(/^&/g,'');
	if( url.indexOf('?')>0 ){
		url += '&' + query;
	}else{
		url += '?' + query;
	}
	window.location.href = url;
})
</script>
	<!-- /头部 -->
	
	<!-- 主体 -->
	
<div id="main-container" class="container">
    <div class="row">
	<div  style="height:20px;"></div>
     	
	<div class="col-sm-11 col-lg-9">			
	<section id="contents">	
	<div class="dhx"><a href="index.php">首页</a> 
	<a href="/index.php?s=/home/newscenter/lists.html">
		<i class="icon-chevron-right"></i> 	</a> >	<a href="/index.php?s=/home/newscenter/lists/category/newcenter.html">
		<i class="icon-chevron-right"></i> 新闻中心	</a> ><span><a href="/index.php?s=/home/newscenter/lists/category/yw.html">
		<i class="icon-chevron-right"></i>广药要闻	</a></span>		
	<span> > <a href="/index.php?s=/home/article/lists/category/yw.html">学校召开校园安全工作会议 </a></span>
	</div> 
	<div class="title text-center">	
		<h3>学校召开校园安全工作会议</h3>		
		<small>发布时间：2018-03-02 来源：保卫处 点击量：257</small>
	</div>	
		<hr/>	
		<div class="content">
		<span style="font-size:18px;font-family:KaiTi_GB2312;">　　3月2日上午，学校在大学城校区第一会议室召开校园安全工作会议。会议由学校党委书记杨海涛主持，党委副书记巫宏星、机关相关职能部门、校区办、各学院、图书馆、体育馆等部门和单位负责人参加了会议。</span><br />
<span style="font-size:18px;font-family:KaiTi_GB2312;">　　会上，巫宏星传达了广东省教育厅关于校园安全工作的有关文件精神，要求职能部门、校区办及学院切实做好开学的各项保障工作，确保校园安全稳定。</span><br />
<span style="font-size:18px;font-family:KaiTi_GB2312;">　　随后，保卫处汇报了上学期末开展今冬明春安全检查暨学生宿舍、“三合一”场所专项检查的情况，并要求各相关单位做好整改。相关职能部门及校区办汇报了寒假和开学准备工作的情况。</span><br />
<span style="font-size:18px;font-family:KaiTi_GB2312;">　　最后，杨海涛传达了教育部和广东省教育厅的校园安全工作会议精神，并对新学期校园安全工作进行了部署。杨海涛强调，各部门和单位要以习近平新时代中国特色社会主义思想为指导，认真贯彻落实党中央、国务院关于学校安全工作的决策部署，牢固树立安全发展理念，确保学校安全稳定。</span>		</div>
		<div  style="height:20px;"></div>
		<hr/>
		<div class="pull col-sm-11 col-lg-9">
			<span class="pull-left">
				<p><span>上一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6690.html">学校举行2018年离退休老同志迎春茶话会</a></p>							</span>
		</div>
		<div class="clearer"></div>
		</section>
		
	</div>	

	 
<div class="col-sm-11 col-lg-3">
	<div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">24小时排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（5）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">一周排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（750）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6699.html" title="学校召开校园安全工作会议 阅读（258）">学校召开校园安全工作会议</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6691.html" title="【南方＋】广药医学生见义勇为救路人，事后他竟然说很惭愧...... 阅读（222）">【南方＋】广药医学生见义...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6700.html" title="不忘初心，坚定信念，为培育英才努力奋斗——医药化工学院召开第二届教职工代表大会暨工会会员代表大会 阅读（165）">不忘初心，坚定信念，为培...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/2530.html" title="校长/党委副书记  郭  姣 阅读（46）">校长/党委副书记  郭 ...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（5）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">本月排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6676.html" title="广东药科大学2018年公开招聘人员公告 阅读（16018）">广东药科大学2018年公...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6690.html" title="学校举行2018年离退休老同志迎春茶话会 阅读（841）">学校举行2018年离退休...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（750）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6688.html" title="全国高校健康服务与管理专业 “十三五”规划系列教材评审委员会一届一次会议在海口召开 阅读（660）">全国高校健康服务与管理专...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6686.html" title="我校校长郭姣教授应邀参加中俄医科大学联盟医院揭牌仪式暨一带一路中俄医科大学联盟医学与健康学术会议并发表主旨演讲 阅读（639）">我校校长郭姣教授应邀参加...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6687.html" title="我校与深圳市人才集团有限公司签订《战略合作框架协议》 阅读（629）">我校与深圳市人才集团有限...</a></li>	 
		</div>
	  </div>
	</div>
       
    </div>
</div>

<script type="text/javascript">
    $(function(){
        $(window).resize(function(){
            $("#main-container").css("min-height", $(window).height() - 230);
        }).resize();
    })
</script>
	<!-- /主体 -->

	<!-- 底部 -->
	<div class="footer">
<div class="container">
广东药科大学党委宣传部 版权所有 Copyright © 2017  制作单位：现代教育技术中心网络部  v1.0
</div>
<script type="text/javascript">
(function(){
	var ThinkPHP = window.Think = {
		"ROOT"   : "", //当前网站地址
		"APP"    : "/index.php?s=", //当前项目地址
		"PUBLIC" : "/Public", //项目公共目录地址
		"DEEP"   : "/", //PATHINFO分割符
		"MODEL"  : ["3", "1", "html"],
		"VAR"    : ["m", "c", "a"]
	}
})();
</script>

 <!-- 用于加载js代码 -->
<!-- 页面footer钩子，一般用于加载插件JS文件和JS代码 -->
<div class="hidden"><!-- 用于加载统计代码等隐藏元素 -->
	
</div>
<script>
$(document).ready(function() {
	$('.theme-login').click(function(){
		$('.theme-popover-mask').fadeIn(100);
		$('.theme-popover').slideDown(200);
		})
		$('.theme-poptit .close').click(function(){
		$('.theme-popover-mask').fadeOut(100);
		$('.theme-popover').slideUp(200);
	})
});
</script>
	<!-- /底部 -->
</body>
</html>"""

html4 = """
<!DOCTYPE HTML>
<html>
<head>
	<!DOCTYPE html>
<meta name=renderer content=webkit>
<meta charset="UTF-8">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN / DENY "> 
<title>广东药科大学</title>
<meta content="广东药科大学 广东药科大学官网 广药" name="description">
<meta content="广东药科大学 广东药科大学官网 广药" name="keywords">
<!--<meta name="viewport" content="width=device-width, initial-scale=1.0">-->
<meta name = "viewport" content = "width=device-width, minimum-scale=1, maximum-scale=1">
<meta name = "apple-mobile-web-app-capable" content = "yes" /> 
<link href="/Public/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
<link href="/Public/static/bootstrap/css/bootstrap.css" rel="stylesheet">
<link href="/Public/static/css/custom.css" rel="stylesheet">
<link href="/Public/Home/css/basic.css" rel="stylesheet">
<link href="/Public/Home/css/style_nc.css" rel="stylesheet">
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
<script src="css/bootstrap/js/html5shiv.min.js"></script>
<script src="css/bootstrap/js/respond.min.js"></script>
<script type="text/javascript" src="/Public/static/jquery-1.10.2.min.js"></script>
<![endif]-->
<!--[if gte IE 9]><!-->
<script type="text/javascript" src="/Public/static/jquery-2.0.3.min.js"></script>
<script type="text/javascript" src="/Public/static/bootstrap/js/bootstrap.min.js"></script>
<!--<![endif]-->

<!-- 页面header钩子，一般用于加载插件CSS文件和代码 -->

</head>
<body>
	<!-- 头部 -->
	<div class="header">
<div class="container"> 
<div class="logo">新闻网</div>
<div class="theme-popover">
<div class="theme-poptit">
<a href="javascript:;" title="关闭" class="close">×</a>
</div>
<div class="theme-popbod dform">
<img src="Public/Home/img/nc/weixin.jpg"  />   
</div>
</div>
<span> 
 <form class="search-form" action="" method="post">
<input type="text" value="" class="search" name="searchtext"/>  <!--/index.php?s=/home/newscenter/search.html-->
<a class="sch-btn" href="javascript:;" id="search" url="/index.php?s=/home/newscenter/search.html"> <i class="btn-search"></i></a>
</form>
</span>
<div class="ggicon"><span><a class="theme-login"  href="javascript:;" title="点击后打开大型二维码图片"><img src="/Public/Home/img/icon/weixin.png" /></a></span>
<span><a href=""><img src="/Public/Home/img/icon/weibo.png" /> </a></span>

</div>
</div>
</div>
<nav role="navigation" class="navbar navbar-inverse"> 
<!--navbar-fixed-top -->
	<div class="container navbarhead">	
        <div class="navbar-header">
          <button aria-controls="navbar" aria-expanded="false" data-target="#navbar" data-toggle="collapse" class="navbar-toggle" type="button">
            <span class="sr-only">切换导航</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
		<a class="navbar-brand" href="/index.php?s=/home/newscenter/index.html">首页</a>
        <div class="navbar-collapse collapse" id="navbar">			
          <ul class="nav navbar-nav">
				<li>
						<a href="/index.php?s=/home/newscenter/lists/category/yw.html">广药要闻</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/mt.html">媒体广药</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tz.html">广药图志</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sd.html">高教视点</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/fc.html">广药风采</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sz.html">理论时政</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/zl.html">专题专栏</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/xwzh.html">新闻纵横</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tgxz.html">投稿须知</a>
					</li>          </ul>             		  
        </div><!--/.nav-collapse -->
		</div>				
</nav>
<script>	
$(".btn-search").click(function(){	
	var url = $("#search").attr('url');
	var query  = $('.search-form').find('input').serialize();
	query = query.replace(/(&|^)(\w*?\d*?\-*?_*?)*?=?((?=&)|(?=$))/g,'');
	query = query.replace(/^&/g,'');
	if( url.indexOf('?')>0 ){
		url += '&' + query;
	}else{
		url += '?' + query;
	}
	window.location.href = url;
})
</script>
	<!-- /头部 -->
	
	<!-- 主体 -->
	
<div id="main-container" class="container">
    <div class="row">
	<div  style="height:20px;"></div>
     	
	<div class="col-sm-11 col-lg-9">			
	<section id="contents">	
	<div class="dhx"><a href="index.php">首页</a> 
	<a href="/index.php?s=/home/newscenter/lists.html">
		<i class="icon-chevron-right"></i> 	</a> >	<a href="/index.php?s=/home/newscenter/lists/category/newcenter.html">
		<i class="icon-chevron-right"></i> 新闻中心	</a> ><span><a href="/index.php?s=/home/newscenter/lists/category/xwzh.html">
		<i class="icon-chevron-right"></i>新闻纵横	</a></span>		
	<span> > <a href="/index.php?s=/home/article/lists/category/xwzh.html">中药学院召开党支部书记抓基层党建工作述职会 </a></span>
	</div> 
	<div class="title text-center">	
		<h3>中药学院召开党支部书记抓基层党建工作述职会</h3>		
		<small>发布时间：2018-01-18 来源：中药学院 点击量：1212</small>
	</div>	
		<hr/>	
		<div class="content">
		<div style="text-align:justify;">
	<span style="font-family:KaiTi_GB2312;font-size:18px;">　　1月16日，中药学院党委召开党支部书记抓基层党建述职考评会，参加会议的有中药学院党委书记、副书记、党委委员、行政领导、民主党派代表、教师代表、工会主席等。学院党委副书记刘文伟主持了会议。</span>
</div>
<span style="font-size:18px;font-family:KaiTi_GB2312;">
<div style="text-align:justify;">
	　　按照学校党委《关于开展2017度学校基层党建述职评议考核工作的通知》的要求，学院14个党支部书记对自己过去一年抓党建工作情况，向学院党委进行述职，其内容主要包括：学习宣传贯彻党的十九大精神情况、履行党建责任情况、推进基层党建工作情况、开展思想政治工作情况、整改突出问题和改进措施情况、基层党建特色情况等。
</div>
</span><span style="font-size:18px;font-family:KaiTi_GB2312;">
<div style="text-align:justify;">
	　　学院党委书记黄建明对述职进行了点评。他指出，学院各党支部在过去的一年，紧密结合各自的工作实际，狠抓基层党建工作，把专业特色融入到党建工作中，把党建工作深入到教学、科研、管理和服务各个方面，充分发挥了党支部的战斗堡垒作用和党员的先锋模范作用，取得了可喜的成绩，比如大学城校区第二学生党支部被广东省委教育工委评为“学习型、服务型、创新型党支部”；支部工作案例“广东药科大学中药学院‘10•20’党课学习项目”再次被推荐至教育部思想政治工作司举办的全国高校“两学一做”支部风采展示活动平台中国大学生在线网站上展示。但也存在一些问题，如组织生活形式比较单一，个别党员党员意识比较淡薄，个别支部书记抓思想政治教育工作不到位等等，希望相关支部书记对照检查并进行反思，明确努力方向，并提出相应的整改措施。
</div>
</span><span style="font-size:18px;font-family:KaiTi_GB2312;">
<div style="text-align:justify;">
	　　最后，黄建明对党支部书记提出了四点希望；一是继续深入学习贯彻落实党的十九大精神，真正做到学懂、弄通、做实，并以此来指导和推动工作。二是继续坚持管党治党，把全面从严治党的责任扛在肩上。落实好“三会一课”制度，创新性地开展组织生活，使组织生活充满活力，加强党员教育，把政治标准放在首位。三是做好思想政治工作，贯彻落实高校思想政治工作会议精神，把师生的思想政治素质放在首位，加强师德师风和学风建设，坚持立德树人，把思想政治工作贯穿教育教学全过程。四是积极探索党建工作的方式方法，做好党建工作，创造党建工作的活力和战斗力。
</div>
</span>		</div>
		<div  style="height:20px;"></div>
		<hr/>
		<div class="pull col-sm-11 col-lg-9">
			<span class="pull-left">
				<p><span>上一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6634.html">医药经济学院举办写作训练讲座----媒体界校友分享经验，详解“正式写作”</a></p>				<p><span>下一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6645.html">以本科教学审核评估为契机，全面推进生科院的内涵建设----生科院召开第二届教职工代表大会暨第二届工会会员代表大会第三次会议</a></p>			</span>
		</div>
		<div class="clearer"></div>
		</section>
		
	</div>	

	 
<div class="col-sm-11 col-lg-3">
	<div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">24小时排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（5）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">一周排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（750）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6699.html" title="学校召开校园安全工作会议 阅读（258）">学校召开校园安全工作会议</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6691.html" title="【南方＋】广药医学生见义勇为救路人，事后他竟然说很惭愧...... 阅读（222）">【南方＋】广药医学生见义...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6700.html" title="不忘初心，坚定信念，为培育英才努力奋斗——医药化工学院召开第二届教职工代表大会暨工会会员代表大会 阅读（165）">不忘初心，坚定信念，为培...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/2530.html" title="校长/党委副书记  郭  姣 阅读（46）">校长/党委副书记  郭 ...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（5）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">本月排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6676.html" title="广东药科大学2018年公开招聘人员公告 阅读（16023）">广东药科大学2018年公...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6690.html" title="学校举行2018年离退休老同志迎春茶话会 阅读（841）">学校举行2018年离退休...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（750）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6688.html" title="全国高校健康服务与管理专业 “十三五”规划系列教材评审委员会一届一次会议在海口召开 阅读（660）">全国高校健康服务与管理专...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6686.html" title="我校校长郭姣教授应邀参加中俄医科大学联盟医院揭牌仪式暨一带一路中俄医科大学联盟医学与健康学术会议并发表主旨演讲 阅读（639）">我校校长郭姣教授应邀参加...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6687.html" title="我校与深圳市人才集团有限公司签订《战略合作框架协议》 阅读（629）">我校与深圳市人才集团有限...</a></li>	 
		</div>
	  </div>
	</div>
       
    </div>
</div>

<script type="text/javascript">
    $(function(){
        $(window).resize(function(){
            $("#main-container").css("min-height", $(window).height() - 230);
        }).resize();
    })
</script>
	<!-- /主体 -->

	<!-- 底部 -->
	<div class="footer">
<div class="container">
广东药科大学党委宣传部 版权所有 Copyright © 2017  制作单位：现代教育技术中心网络部  v1.0
</div>
<script type="text/javascript">
(function(){
	var ThinkPHP = window.Think = {
		"ROOT"   : "", //当前网站地址
		"APP"    : "/index.php?s=", //当前项目地址
		"PUBLIC" : "/Public", //项目公共目录地址
		"DEEP"   : "/", //PATHINFO分割符
		"MODEL"  : ["3", "1", "html"],
		"VAR"    : ["m", "c", "a"]
	}
})();
</script>

 <!-- 用于加载js代码 -->
<!-- 页面footer钩子，一般用于加载插件JS文件和JS代码 -->
<div class="hidden"><!-- 用于加载统计代码等隐藏元素 -->
	
</div>
<script>
$(document).ready(function() {
	$('.theme-login').click(function(){
		$('.theme-popover-mask').fadeIn(100);
		$('.theme-popover').slideDown(200);
		})
		$('.theme-poptit .close').click(function(){
		$('.theme-popover-mask').fadeOut(100);
		$('.theme-popover').slideUp(200);
	})
});
</script>
	<!-- /底部 -->
</body>
</html>"""

html5 = """
<!DOCTYPE HTML>
<html>
<head>
	<!DOCTYPE html>
<meta name=renderer content=webkit>
<meta charset="UTF-8">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN / DENY "> 
<title>广东药科大学</title>
<meta content="广东药科大学 广东药科大学官网 广药" name="description">
<meta content="广东药科大学 广东药科大学官网 广药" name="keywords">
<!--<meta name="viewport" content="width=device-width, initial-scale=1.0">-->
<meta name = "viewport" content = "width=device-width, minimum-scale=1, maximum-scale=1">
<meta name = "apple-mobile-web-app-capable" content = "yes" /> 
<link href="/Public/static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
<link href="/Public/static/bootstrap/css/bootstrap.css" rel="stylesheet">
<link href="/Public/static/css/custom.css" rel="stylesheet">
<link href="/Public/Home/css/basic.css" rel="stylesheet">
<link href="/Public/Home/css/style_nc.css" rel="stylesheet">
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
<script src="css/bootstrap/js/html5shiv.min.js"></script>
<script src="css/bootstrap/js/respond.min.js"></script>
<script type="text/javascript" src="/Public/static/jquery-1.10.2.min.js"></script>
<![endif]-->
<!--[if gte IE 9]><!-->
<script type="text/javascript" src="/Public/static/jquery-2.0.3.min.js"></script>
<script type="text/javascript" src="/Public/static/bootstrap/js/bootstrap.min.js"></script>
<!--<![endif]-->

<!-- 页面header钩子，一般用于加载插件CSS文件和代码 -->

</head>
<body>
	<!-- 头部 -->
	<div class="header">
<div class="container"> 
<div class="logo">新闻网</div>
<div class="theme-popover">
<div class="theme-poptit">
<a href="javascript:;" title="关闭" class="close">×</a>
</div>
<div class="theme-popbod dform">
<img src="Public/Home/img/nc/weixin.jpg"  />   
</div>
</div>
<span> 
 <form class="search-form" action="" method="post">
<input type="text" value="" class="search" name="searchtext"/>  <!--/index.php?s=/home/newscenter/search.html-->
<a class="sch-btn" href="javascript:;" id="search" url="/index.php?s=/home/newscenter/search.html"> <i class="btn-search"></i></a>
</form>
</span>
<div class="ggicon"><span><a class="theme-login"  href="javascript:;" title="点击后打开大型二维码图片"><img src="/Public/Home/img/icon/weixin.png" /></a></span>
<span><a href=""><img src="/Public/Home/img/icon/weibo.png" /> </a></span>

</div>
</div>
</div>
<nav role="navigation" class="navbar navbar-inverse"> 
<!--navbar-fixed-top -->
	<div class="container navbarhead">	
        <div class="navbar-header">
          <button aria-controls="navbar" aria-expanded="false" data-target="#navbar" data-toggle="collapse" class="navbar-toggle" type="button">
            <span class="sr-only">切换导航</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
        </div>
		<a class="navbar-brand" href="/index.php?s=/home/newscenter/index.html">首页</a>
        <div class="navbar-collapse collapse" id="navbar">			
          <ul class="nav navbar-nav">
				<li>
						<a href="/index.php?s=/home/newscenter/lists/category/yw.html">广药要闻</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/mt.html">媒体广药</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tz.html">广药图志</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sd.html">高教视点</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/fc.html">广药风采</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/sz.html">理论时政</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/zl.html">专题专栏</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/xwzh.html">新闻纵横</a>
					</li><li>
						<a href="/index.php?s=/home/newscenter/lists/category/tgxz.html">投稿须知</a>
					</li>          </ul>             		  
        </div><!--/.nav-collapse -->
		</div>				
</nav>
<script>	
$(".btn-search").click(function(){	
	var url = $("#search").attr('url');
	var query  = $('.search-form').find('input').serialize();
	query = query.replace(/(&|^)(\w*?\d*?\-*?_*?)*?=?((?=&)|(?=$))/g,'');
	query = query.replace(/^&/g,'');
	if( url.indexOf('?')>0 ){
		url += '&' + query;
	}else{
		url += '?' + query;
	}
	window.location.href = url;
})
</script>
	<!-- /头部 -->
	
	<!-- 主体 -->
	
<div id="main-container" class="container">
    <div class="row">
	<div  style="height:20px;"></div>
     	
	<div class="col-sm-11 col-lg-9">			
	<section id="contents">	
	<div class="dhx"><a href="index.php">首页</a> 
	<a href="/index.php?s=/home/newscenter/lists.html">
		<i class="icon-chevron-right"></i> 	</a> >	<a href="/index.php?s=/home/newscenter/lists/category/newcenter.html">
		<i class="icon-chevron-right"></i> 新闻中心	</a> ><span><a href="/index.php?s=/home/newscenter/lists/category/yw.html">
		<i class="icon-chevron-right"></i>广药要闻	</a></span>		
	<span> > <a href="/index.php?s=/home/article/lists/category/yw.html">我校罗祥智老师获“广东省研究生德育工作先进个人”表彰 </a></span>
	</div> 
	<div class="title text-center">	
		<h3>我校罗祥智老师获“广东省研究生德育工作先进个人”表彰</h3>		
		<small>发布时间：2018-01-25 来源：公共卫生学院 研究生学院 点击量：2662</small>
	</div>	
		<hr/>	
		<div class="content">
		<div style="text-align:justify;">
	<span style="font-family:KaiTi_GB2312;font-size:18px;">　　日前，广东省学位与研究生教育学会德育工作委员会发出通知，对26家高校及科研院所的33名研究生德育工作者授予“2017年广东省研究生德育工作先进个人”称号并进行表彰。我校公共卫生学院研究生党支部书记罗祥智老师榜上有名。</span>
</div>
<span style="font-size:18px;font-family:KaiTi_GB2312;">
<div style="text-align:justify;">
	　　罗祥智老师身兼我校公共卫生学院研究生党支部书记及公共卫生与预防医学一级学科研究生教学工作秘书、研究生兼职辅导员。多年来，他坚持“用真诚凝聚人心，用服务汇聚力量”的工作理念，在平凡的工作岗位上坚守，以饱满的工作热情、务实的工作作风，全身心的投入各项工作，履行着一名研究生德育工作者“为人师表，教书育人”的职责。
</div>
</span><span style="font-size:18px;font-family:KaiTi_GB2312;">
<div style="text-align:justify;">
	　　作为一名研究生党支部书记，罗祥智注重结合学生学习、生活和科研工作的特点，注重以党建工作的有效性为核心，牢牢抓住思想政治建设的主阵地，坚持“抓好党建促科研，学好专业树典型”的工作思路，采取灵活多样的学习方式，开展丰富多彩的学生活动，深受学生喜欢，促进了公共卫生学院研究生良好学风的形成。在工作中，罗祥智努力做到对学生的精准管理，熟悉掌握每一位学生的情况，注重培养学生理性平和的健康心态，加强人文关怀和心理疏导。同时，他不断创新工作模式，提高工作效率，利用现代网络技术，搭建起QQ、飞信、微信等各种便捷高效的师生沟通交流平台，周到、耐心、细致地向广大师生做好答疑解惑排难工作。他所创作的微党课视频还获得了学校微党课视频创作大赛“特等奖”，作品代表学校被选送到教育部思想政治工作司举办的全国高校“两学一做”支部风采展示活动平台中国大学生在线网站上展示。2015年，他配合研究生学院率先推行研究生二级管理的试点工作，得到广大师生的认可。在他的带领下，公共卫生学院研究生党员的先锋模范作用得到充分发挥，团队的凝聚力和战斗力不断增强，在参加各类省级、国家级学术竞赛活动中屡获佳绩，发表高水平学术论文的数量逐年增长，质量逐年提升，党支部也先后获得广东药科大学“先进党支部”、“优秀党支部”等荣誉称号。在由省委组织部与省委教育工委联合举办的“2017年广东省高校基层党支部书记示范培训班”上，罗祥智老师作为优秀学员代表作党建工作经验交流，获得了大家的一致好评。
</div>
</span>
<div style="text-align:justify;">
	<br />
</div>		</div>
		<div  style="height:20px;"></div>
		<hr/>
		<div class="pull col-sm-11 col-lg-9">
			<span class="pull-left">
				<p><span>上一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6675.html">我校护理学院加入中国医护整合联盟助力健康中国建设</a></p>				<p><span>下一篇：</span><a href="/index.php?s=/home/newscenter/detail/id/6682.html">我校广东省医药3D打印机及个性化医疗工程技术研究中心举行授牌仪式</a></p>			</span>
		</div>
		<div class="clearer"></div>
		</section>
		
	</div>	

	 
<div class="col-sm-11 col-lg-3">
	<div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">24小时排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（6）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">一周排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（750）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6699.html" title="学校召开校园安全工作会议 阅读（260）">学校召开校园安全工作会议</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6691.html" title="【南方＋】广药医学生见义勇为救路人，事后他竟然说很惭愧...... 阅读（222）">【南方＋】广药医学生见义...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6700.html" title="不忘初心，坚定信念，为培育英才努力奋斗——医药化工学院召开第二届教职工代表大会暨工会会员代表大会 阅读（165）">不忘初心，坚定信念，为培...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/2530.html" title="校长/党委副书记  郭  姣 阅读（46）">校长/党委副书记  郭 ...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6701.html" title="中共中央关于深化党和国家机构改革的决定  （二〇一八年二月二十八日中国共产党第十九届中央委员会第三次全体会议通过） 阅读（6）">中共中央关于深化党和国家...</a></li>	 
		</div>
	  </div>
	  <div class="panel pannel1">
		<div class="panel-heading">
		  <h3 class="panel-title">本月排行</h3>  
		</div>
		<div class="panel-body pblist1">			
			<li><a href="/index.php?s=/home/newscenter/detail/id/6676.html" title="广东药科大学2018年公开招聘人员公告 阅读（16028）">广东药科大学2018年公...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6690.html" title="学校举行2018年离退休老同志迎春茶话会 阅读（842）">学校举行2018年离退休...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6689.html" title="郭姣校长慰问海南校友 阅读（750）">郭姣校长慰问海南校友</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6688.html" title="全国高校健康服务与管理专业 “十三五”规划系列教材评审委员会一届一次会议在海口召开 阅读（660）">全国高校健康服务与管理专...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6686.html" title="我校校长郭姣教授应邀参加中俄医科大学联盟医院揭牌仪式暨一带一路中俄医科大学联盟医学与健康学术会议并发表主旨演讲 阅读（639）">我校校长郭姣教授应邀参加...</a></li><li><a href="/index.php?s=/home/newscenter/detail/id/6687.html" title="我校与深圳市人才集团有限公司签订《战略合作框架协议》 阅读（629）">我校与深圳市人才集团有限...</a></li>	 
		</div>
	  </div>
	</div>
       
    </div>
</div>

<script type="text/javascript">
    $(function(){
        $(window).resize(function(){
            $("#main-container").css("min-height", $(window).height() - 230);
        }).resize();
    })
</script>
	<!-- /主体 -->

	<!-- 底部 -->
	<div class="footer">
<div class="container">
广东药科大学党委宣传部 版权所有 Copyright © 2017  制作单位：现代教育技术中心网络部  v1.0
</div>
<script type="text/javascript">
(function(){
	var ThinkPHP = window.Think = {
		"ROOT"   : "", //当前网站地址
		"APP"    : "/index.php?s=", //当前项目地址
		"PUBLIC" : "/Public", //项目公共目录地址
		"DEEP"   : "/", //PATHINFO分割符
		"MODEL"  : ["3", "1", "html"],
		"VAR"    : ["m", "c", "a"]
	}
})();
</script>

 <!-- 用于加载js代码 -->
<!-- 页面footer钩子，一般用于加载插件JS文件和JS代码 -->
<div class="hidden"><!-- 用于加载统计代码等隐藏元素 -->
	
</div>
<script>
$(document).ready(function() {
	$('.theme-login').click(function(){
		$('.theme-popover-mask').fadeIn(100);
		$('.theme-popover').slideDown(200);
		})
		$('.theme-poptit .close').click(function(){
		$('.theme-popover-mask').fadeOut(100);
		$('.theme-popover').slideUp(200);
	})
});
</script>
	<!-- /底部 -->
</body>
</html>"""

html6 = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<HTML xmlns:wb="http://open.weibo.com/wb"><HEAD>
<TITLE>学校2017年工作总结交流大会召开-广东工业大学新闻网</TITLE><META Name="keywords" Content="广东工业大学新闻网，工大新闻网" />




<script src="dfiles/14832/open/api/js/wb.js" type="text/javascript" charset="utf-8"></script>
<META content="text/html; charset=UTF-8" http-equiv="Content-Type">
<META content="no-transform" http-equiv="Cache-Control"><script type="text/javascript" src="dfiles/20140/js/offlights.js"></script><script type="text/javascript">
function doZoom(size){
        document.getElementById("contentText").style.fontSize = size + "pt";
    }
</script><script type="text/javascript" src="dfiles/20140/plugins/flash/jwplayer.js"></script><LINK rel="stylesheet" type="text/css" href="dfiles/20140/css/style.css"><script src="dfiles/20140/admin/scripts/bdtxk.js" type="text/javascript"></script>

<!--Announced by Visual SiteBuilder 9-->
<link rel="stylesheet" type="text/css" href="_sitegray/_sitegray_d.css" />
<script language="javascript" src="_sitegray/_sitegray.js"></script>
<!-- CustomerNO:77656262657232307003475455525640035748 -->
<link rel="stylesheet" type="text/css" href="neirongye.vsb.css" />
<script type="text/javascript" src="/system/resource/js/counter.js"></script>
<script type="text/javascript">_jsq_(1045,'/neirongye.jsp',7471,1164291239)</script>
</HEAD>
<BODY ><LINK rel="stylesheet" type="text/css" href="http://v3.jiathis.com/code/css/jiathis_share.css"><IFRAME frameborder="0" style="position: absolute;filter: alpha(opacity=0);display: none;opacity: 0"></IFRAME>
<DIV class="jiathis_style" style="z-index: 1000000000;position: absolute;display: none;overflow: auto;top: 50%;left: 50%"></DIV>
<DIV class="jiathis_style" style="z-index: 1000000000;position: absolute;display: none;overflow: auto"></DIV><IFRAME src="http://v3.jiathis.com/code/jiathis_utility.html" frameborder="0" style="display: none"></IFRAME>
<DIV class="jiathis_style" style="z-index: 1000000000;position: absolute;display: none;overflow: auto;top: 50%;left: 50%"></DIV>
<DIV class="jiathis_style" style="z-index: 1000000000;position: absolute;display: none;overflow: auto"></DIV><script type="text/javascript">
//<![CDATA[
var theForm = document.forms['aspnetForm'];
if (!theForm) {
    theForm = document.aspnetForm;
}
function __doPostBack(eventTarget, eventArgument) {
    if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
        theForm.__EVENTTARGET.value = eventTarget;
        theForm.__EVENTARGUMENT.value = eventArgument;
        theForm.submit();
    }
}
//]]>
</script><script language="JavaScript">
<!--
function tick() {
var hours, minutes, seconds;
var intHours, intMinutes, intSeconds;
var today;
var intMon;
today = new Date();
intHours = today.getHours();
intMinutes = today.getMinutes();
intSeconds = today.getSeconds();
intMon = today.getMonth()

if (intHours == 0) {
hours = "00:";
} else if (intHours < 10) { 
hours = "0" + intHours+":";
} else {
hours = intHours + ":";
}
intHours = intHours + 2;
if (intHours == 0) {
syhours = "00:";
} else if (intHours < 10) { 
syhours = "0" + intHours+":";
} else {
syhours = intHours + ":";
}

if (intHours == 0) {
hours = "00:";
} else if (intHours < 10) { 
hours = "0" + intHours+":";
} else {
hours = intHours + ":";
}
intHours = intHours + 2;
if (intHours == 0) {
syhours = "00:";
} else if (intHours < 10) { 
nzhours = "0" + intHours+":";
} else {
nzhours = intHours + ":";
}

if (intMinutes < 10) {
minutes = "0"+intMinutes+":";
} else {
minutes = intMinutes+":";
}
if (intSeconds < 10) {
seconds = "0"+intSeconds+" ";
} else {
seconds = intSeconds+" ";
} 
intMon =intMon +1;

timeString =today.getFullYear()+"年"+ intMon +"月"+ today.getDate()+"日";

Clock.innerHTML = timeString;
window.setTimeout("tick();", 1000);
}

window.onload = tick;
//-->
</script><script src="dfiles/20140/5dc0a866bda26a10031347d2c413eda5_webresource.axd.js" type="text/javascript"></script><!--头部导航开始-->
<DIV class="topdaohang">
<DIV class="topdaohangc">
<TABLE cellspacing="0" cellpadding="0" width="100%">
<TBODY>
<TR>
<TD width="50%"><script language="javascript" src="/system/resource/js/dynclicks.js"></script><script language="javascript" src="/system/resource/js/openlink.js"></script><a href="zhengwenye.jsp?urltype=tree.TreeTempUrl&amp;wbtreeid=1043" >关于我们</a> | 
<a href="zhengwenye.jsp?urltype=tree.TreeTempUrl&amp;wbtreeid=1044" >部门概况</a> | 
<a href="http://www.gdut.edu.cn/" >学校主页</a> | 

<script language="javascript">
function dosuba63721a()
{
    try{
        var ua = navigator.userAgent.toLowerCase();
        if(ua.indexOf("msie 8")>-1)
        {
            window.external.AddToFavoritesBar(document.location.href,document.title,"");//IE8
        }else if(ua.toLowerCase().indexOf("rv:")>-1)
        {
            window.external.AddToFavoritesBar(document.location.href,document.title,"");//IE11+
        }else{
            if (document.all) 
            {
                window.external.addFavorite(document.location.href, document.title);
            }else if(window.sidebar)
            {
                window.sidebar.addPanel( document.title, document.location.href, "");//firefox
            }
            else
            {
                alert(hotKeysa63721a());
            }
        }

    }
    catch (e){alert("无法自动添加到收藏夹，请使用 Ctrl + d 手动添加");}
}
function hotKeysa63721a() 
{
    var ua = navigator.userAgent.toLowerCase(); 
    var str = "";    
    var isWebkit = (ua.indexOf('webkit') != - 1); 
    var isMac = (ua.indexOf('mac') != - 1);     
    if (ua.indexOf('konqueror') != - 1) 
    {  
        str = 'CTRL + B'; // Konqueror   
    } 
    else if (window.home || isWebkit || isMac) 
    {        
        str = (isMac ? 'Command/Cmd' : 'CTRL') + ' + D'; // Netscape, Safari, iCab, IE5/Mac   
    }
    return ((str) ? '无法自动添加到收藏夹，请使用' + str + '手动添加' : str);
}
function setHomepagea63721a()
{
    var url = document.location.href;
    if (document.all)
    {
        document.body.style.behavior='url(#default#homepage)';
        document.body.setHomePage(url);
    }
    else if (window.sidebar)
    {
        if(window.netscape)
        {
             try{
                  netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
             }catch (e){
                   alert("该操作被浏览器拒绝，如果想启用该功能，请在地址栏内输入 about:config,然后将项 signed.applets.codebase_principal_support 值该为true");
             }
        }
    var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components. interfaces.nsIPrefBranch);
    prefs.setCharPref('browser.startup.homepage',url);
    }
    else
    {
        alert("浏览器不支持自动设为首页，请手动设置");
    }
}
</script>
<A onclick="javascript:dosuba63721a();" href="#">加入收藏</A> | <A href="index/wzdt.htm" style="TEXT-DECORATION: none;">网站地图</A> </TD>
<TD width="50%"><SPAN class="floatright">
<UL class="xmt">
<LI class="xmtweixin"><A href="weibo.jsp?urltype=tree.TreeTempUrl&amp;wbtreeid=1041">微信官号</A>
</LI>
<LI class="xmtweibo"><A href="weibo.jsp?urltype=tree.TreeTempUrl&amp;wbtreeid=1041">微博官号</A>
</LI>
<LI class="xmtjbhg"><A href="http://gdutnews.gdut.edu.cn:6666/" target="_blank">旧版回顾</A>
</LI>
<LI class="xmtjyfk"><A href="mailto:xwzx@gdut.edu.cn" target="_blank">建议反馈</A>
</LI></UL>
<DIV class="clear"></DIV></SPAN></TD></TR></TBODY></TABLE></DIV></DIV><!--头部导航结束--><!--banner开始-->
<DIV class="banner"><IMG src="dfiles/20140/images/banner.jpg"></DIV><!--banner结束--><!--栏目导航开始-->
<DIV class="menu"><UL>
<LI><A href="index.htm" >网站首页</A></LI>
<LI><A href="liebiaotupian.jsp?urltype=tree.TreeTempUrl&wbtreeid=1013" >学校新闻</A></LI>
<LI><A href="liebiaotupian.jsp?urltype=tree.TreeTempUrl&wbtreeid=1113" >图片新闻</A></LI>
<LI><A href="meitigongda.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016" >媒体工大</A></LI>
<LI><A href="http://xbw.gdut.edu.cn/digitalnews/" target="_blank">数字校报</A></LI>
<LI><A href="liebiaotupian.jsp?urltype=tree.TreeTempUrl&wbtreeid=1017" >人文校园</A></LI>
<LI><A href="liebiaotupian.jsp?urltype=tree.TreeTempUrl&wbtreeid=1018" >校友动态</A></LI>
<LI><A href="liebiaotupian.jsp?urltype=tree.TreeTempUrl&wbtreeid=1019" >学习园地</A></LI>
<LI><A href="liebiaotupian.jsp?urltype=tree.TreeTempUrl&wbtreeid=1020" >专题报道</A></LI>
<LI><A href="http://xmt.gdut.edu.cn" target="_blank">新媒体联盟</A></LI>
<LI><A href="wsxsg.htm" >网上校史馆</A></LI>
</UL></DIV><!--栏目导航结束--><!--时间天气以及搜索开始-->
<DIV class="sousuo">
<DIV class="sousuoc">
<TABLE cellspacing="0" cellpadding="0" height="28">
<TBODY>
<TR>
<TD valign="top" width="24" align="center">
<DIV style="padding-top: 7px"><IMG src="dfiles/20140/images/nowtimeico.jpg"></DIV></TD>
<TD valign="middle" width="110">
<DIV id="Clock"></DIV></TD>
<TD valign="middle" width="370"><IFRAME height="23" src="http://i.tianqi.com/index.php?c=code&id=1&icon=1&wind=0&num=1" frameborder="0" width="350" allowtransparency scrolling="no"></IFRAME></TD>
<TD valign="top" width="500"><SPAN class="floatright">
<DIV class="sousuocon">





<form action='sousuo.jsp?wbtreeid=1045' method='post' name='a63761a'  style="display: inline;" onsubmit="return subsearchdataa63761a()">
  <input type='hidden' name='Find' value='find'><input type='hidden' name='entrymode' value='1'><input type='hidden' id='INTEXT2'  name='INTEXT2' value=''><input type='hidden' name='news_search_code'>
  <span id="intextspana63761a"></span>
<DIV style="height: 24px;width: 224px;float: left"><INPUT id="ctl00_tbxkey" class="suosuotxt" name='INTEXT'></DIV>
<DIV style="height: 24px;width: 50px;float: left"><INPUT id="ctl00_btnseach" class="suosuobtn" type="submit" value="" ></DIV>

</form>
<script>
String.prototype.trim　= function()       
{              
    var t = this.replace(/(^\s*)|(\s*$)/g, "");     
    return t.replace(/(^　*)|(　*$)/g, "");     
}  
function subsearchdataa63761a()
{ 
    if(document.a63761a.INTEXT.value.trim()=="")
    {
        alert("请输入查询关键字！");
        return false;
    }
    if(checkDataa63761a(document.a63761a))
    {
       return true;  
    }
    return false;
}       
</script>

    <script language='JavaScript' src='_dwr/engine.js'></script>
    <script language='JavaScript' src='_dwr/util.js'></script>
    <script language='JavaScript' src='_dwr/interface/NewsSearchDWR.js'></script>
    <script language='JavaScript' src='/system/resource/js/vsb_news_search.js'></script>
    <script language='JavaScript' src='/system/resource/js/vsb_news_search_entry.js'></script>  
    <script language='JavaScript' src='/system/resource/js/language.js'></script>
    <script language='JavaScript' src='/system/resource/js/base64.js'></script>
    <script language='JavaScript' src='/system/resource/js/formfunc.js'></script>    
    
    <script>    
    news_searcha63761a = new vsb_news_search();
    news_searcha63761a.isShowCode=false;
    news_searcha63761a.tooltipid = 'tooltipa63761a';
    news_searcha63761a.apptag = 'intextspana63761a';
    news_searcha63761a.frametag = 'intextframea63761a';
    news_search_entrya63761a = new vsb_news_search_entry();
    news_search_entrya63761a.formname = "a63761a";
    news_search_entrya63761a.news_search_obj = news_searcha63761a; 
    news_search_entrya63761a.querytxtsize = 155
    news_search_entrya63761a.yzmts ="您的查询过于频繁，请输入验证码后继续查询";
    news_search_entrya63761a.qdstyle ="";
    news_search_entrya63761a.qdname = "确定";
    news_search_entrya63761a.qxstyle = "";
    news_search_entrya63761a.qxname = "取消";    
    function checkDataa63761a(formname)
    {    
        return news_search_entrya63761a.checkdata(formname)   
    }
    </script>
<script language="javascript" src="/system/resource/js/base64.js"></script> </DIV></SPAN></TD></TR></TBODY></TABLE></DIV></DIV>
<DIV></DIV>
<DIV></DIV>
<DIV class="newslistcon">
<DIV class="listright"><SPAN id="ctl00_ContentPlaceHolder1_ListRight1_Label1"><!--新闻回顾-->
<DIV class="listrightc">
<DIV class="listrightcon">
<DIV class="listrightdh">新闻查询</DIV>
<DIV id="datepicker" class="news_back_date">
<DIV class="com_inputbox">



<script type="text/javascript">
  var newsdays63790 = ['2018-03-02','2018-03-05'];
  var flag=true;
  function hasnews63790(c_year,c_month,c_day)
  {
     c_month = c_month+1;
     for(var i=0;i<newsdays63790.length;i++)
     {
        var t_date = newsdays63790[i].split("-");
        if(c_year==t_date[0]&&c_month==t_date[1]&&c_day==t_date[2])
        {
            return true;
        }
     }
     flag=false;
     return false;
  }
  
  function tosubmit63790(c_year,c_month,c_day)
  {
      document.forms['when63790'].calendarselecteddate.value = c_year+"-"+(c_month+1)+"-"+c_day;
      document.forms['when63790'].showyear.value = "";
      document.forms['when63790'].showmonth.value = "";
      document.forms['when63790'].action="liebiaoriliwenzhang.jsp?wbtreeid=1045";
      document.forms['when63790'].submit();
  }
    
  var Selected_Month63790;
  var Selected_Year63790; 
  var shownews_date63790 = "2018-3-5";
  var Days_in_Month63790 = new Array(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31); 
  var Current_Year63790 = new Date().getFullYear();
  var Current_Month63790 = new Date().getMonth();
  var Today63790 = new Date().getDate(); 
  function fzctjqu(s)
  {
    var obj = document.getElementById(s);
    if(obj) return obj;
    return s.value;
  }
 
  function Make_Calendar63790(Year, Month) { 
   var First_Date = new Date(Year, Month, 1); 
   var First_Day = First_Date.getDay() + 1; 
   if (((Days_in_Month63790[Month] == 31) && (First_Day >= 6)) || 
   ((Days_in_Month63790[Month] == 30) && (First_Day == 7))) { 
   var Rows = 6; 
   } 
   else if ((Days_in_Month63790[Month] == 28) && (First_Day == 1)) { 
   var Rows = 4; 
   } 
   else { 
   var Rows = 5; 
   } 
   
   var HTML_String = '<table width="100%"><tr><td valign="top"><table cellpadding="2" cellspacing="2" width="100%">';    
   //HTML_String += '<tr  class="fontstyle63790"  ><th>Su</th><th>Mo</th><th>Tu</th><th>We</th><th>Th</th><th>Fr</th><th>Sa</th></tr>';  
   HTML_String += '<tr  class="fontstyle63790"  ><th>日</th><th>一</th><th>二</th><th>三</th><th>四</th><th>五</th><th>六</th></tr>';  
   
   var Day_Counter = 1; 
   var Loop_Counter = 1; 
   for (var j = 1; j <= Rows; j++) { 
   HTML_String += '<tr align="centert" valign="top">'; 
   for (var i = 1; i < 8; i++) { 
   if ((Loop_Counter >= First_Day) && (Day_Counter <= Days_in_Month63790[Month])) { 
   if ((Day_Counter == Today63790) && (Year == Current_Year63790) && (Month == Current_Month63790)) { 
   HTML_String += '<td align=center style="cursor:pointer;cursor:pointer;" title="今天" onclick="javascript:tosubmit63790('+Year+','+Month+','+Day_Counter+')"  class="todaystyle63790" >' + Day_Counter + '</td>'; 
   } else if(shownews_date63790 && (shownews_date63790==Year+'-'+(Month+1)+'-'+Day_Counter)) {
   HTML_String += '<td align=center style="cursor:pointer;cursor:pointer;" title="您选中了这一天" onclick="javascript:tosubmit63790('+Year+','+Month+','+Day_Counter+')"  class="focusstyle63790"  >' + Day_Counter + '</td>';
   } else if(hasnews63790(Year,Month,Day_Counter)){ 
   HTML_String += '<td align=center style="cursor:pointer;cursor:pointer;" title="在这一天有文章发布" onclick="javascript:tosubmit63790('+Year+','+Month+','+Day_Counter+')"  class="astyle63790"  >' + Day_Counter + '</td>'; 
   } else{ 
   HTML_String += '<td align=center  class="nonewsstyle63790"  >' + Day_Counter + '</td>'; 
   } 
   Day_Counter++; 
   } 
   else { 
   HTML_String += '<td> </td>'; 
   } 
   Loop_Counter++; 
   } 
   HTML_String += '</tr>'; 
   } 
   HTML_String += '</table></td></tr></table>'; 
   fzctjqu('Calendar63790').innerHTML = HTML_String; 
  } 
   
  function Check_Nums63790() { 
   if ((event.keyCode < 48) || (event.keyCode > 57)) { 
   return false; 
   } 
  } 
   
  function On_Year63790() { 
   var Year = fzctjqu('year63790').value; 
   if (Year.length == 4) { 
   Selected_Month63790 = fzctjqu('month63790').selectedIndex; 
   Selected_Year63790 = Year; 
   //Make_Calendar63790(Selected_Year63790, Selected_Month63790); 
    document.forms['when63790'].showyear.value = Selected_Year63790;
    document.forms['when63790'].showmonth.value = Selected_Month63790;
    document.forms['when63790'].action="";
    document.forms['when63790'].submit();
   } 
  } 
   
  function On_Month63790() { 
   var Year = fzctjqu('year63790').value; 
   if (Year.length == 4) { 
   Selected_Month63790 = fzctjqu('month63790').selectedIndex; 
   Selected_Year63790 = Year; 
   //Make_Calendar63790(Selected_Year63790, Selected_Month63790); 
    document.forms['when63790'].showyear.value = Selected_Year63790;
    document.forms['when63790'].showmonth.value = Selected_Month63790;
    document.forms['when63790'].action="";
    document.forms['when63790'].submit();
   } 
   else { 
   alert('Please enter a valid year.'); 
   fzctjqu('year63790').focus(); 
   } 
  } 
   
   
  function Defaults63790() {
   var cyear =  Current_Year63790;
   var cmonth= Current_Month63790;
   
   var showyear="";
   var showmonth = "";

   if(showyear&&showmonth)
   {
     cyear = showyear;
     cmonth= showmonth-1;
   }
   else if(shownews_date63790)
   {
     var td = shownews_date63790.split("-");
     cyear = td[0];
     cmonth= td[1]-1;
   }
   //alert(shownews_date63790.split("-")[0]+"--select--"+(shownews_date63790.split("-")[1]-1))
   for(i=0; i<fzctjqu('month63790').length; i++)
   {
if((showyear?cmonth+1:cmonth) == i) fzctjqu('month63790').options[i].selected = true;
   }
   fzctjqu('year63790').value = cyear; 
   Selected_Month63790 = showyear?cmonth+1:cmonth; 
   Selected_Year63790 = cyear; 
   Make_Calendar63790(Selected_Year63790, Selected_Month63790); 
  } 

  function Skip63790(Direction) { 
   if (Direction == '+') { 
   if (Selected_Month63790== 11) { 
   Selected_Month63790 = 0; 
   Selected_Year63790++; 
   } 
   else { 
   Selected_Month63790++; 
   } 
   } 
   else { 
   if (Selected_Month63790 == 0) { 
   Selected_Month63790 = 11; 
   Selected_Year63790--; 
   } 
   else { 
   Selected_Month63790--; 
   } 
   } 
   //Make_Calendar63790(Selected_Year63790, Selected_Month63790); 
   document.forms['when63790'].showyear.value = Selected_Year63790;
   document.forms['when63790'].showmonth.value = Selected_Month63790;
   document.forms['when63790'].action="";
   document.forms['when63790'].submit();
   //$('month63790').selectedIndex = Selected_Month63790; 
   //$('year63790').value = Selected_Year63790; 
  } 
   
  function set_year63790(str)
  {
    if(str=='-'){fzctjqu('year63790').value=Number(fzctjqu('year63790').value)-1}else{fzctjqu('year63790').value=Number(fzctjqu('year63790').value)+1};
    On_Year63790();
  }
  
  if (document.all) window.attachEvent('onload',Defaults63790);// IE in   
  else window.addEventListener('load',Defaults63790,false);// Firefox 
  </script> 
<table width="240" cellspacing="0" cellpadding="0" align="center"  class="winstyle63790"  > 
<form name="when63790" method=post action=""> 
    <input type=hidden name=showyear value="" />
    <input type=hidden name=showmonth value="" />
    <input type=hidden name=calendarselecteddate value="" /> 
 <tr> 
<td align="center" style="font-size:9pt"> 
<div id="NavBar" style="position:relative;top:-1px; font-family: 宋体; font-size:12px;">
<a href="javascript:set_year63790('-')"  class="fontstyle63790"  title="上一年" >&lt;&lt;</a>&nbsp;
<a href="javascript:Skip63790('-');"  class="fontstyle63790"  title="上一月" >&lt;</a>
<span  class="fontstyle63790"  ><input type="text" name="year63790" size="4" maxlength="4" onKeyPress="return Check_Nums63790()" value="" onKeyUp="On_Year63790()" id="year63790" style="text-align:center;font-size:12px;height:20px">年<select name="month63790" id="month63790" onChange="On_Month63790()" style="width:40px;font-size:12px;height:20px">
<option value="1">1</option>
<option value="2">2</option>
<option value="3">3</option>
<option value="4">4</option>
<option value="5">5</option>
<option value="6">6</option>
<option value="7">7</option>
<option value="8">8</option>
<option value="9">9</option>
<option value="10">10</option>
<option value="11">11</option>
<option value="12">12</option>
</select>月</span>
<a href="javascript:Skip63790('+')"  class="fontstyle63790"  title="下一月">&gt;</a>&nbsp;
<a href="javascript:set_year63790('+')"  class="fontstyle63790"  title="下一年">&gt;&gt;</a>
</div> 

<div id="Calendar63790" style="position:relative;top:-3px;"></div>
</td>
</tr>
</form>
</table></DIV></DIV></DIV></DIV><!--新闻回顾--><!--媒体工大-->
<DIV class="listrightc">
<DIV class="listrightcon">
<DIV class="listrightdh"><SPAN class="floatright"><A href="meitigongda.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016"><IMG src="dfiles/20140/images/gdimg2.jpg"></A></SPAN><SPAN id="ctl00_ContentPlaceHolder1_ListRight1_lblmtgd">媒体工大</SPAN></DIV><UL class="textlistul">
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7501">广州日报：广工大学生团队专注无人机项目研</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7466">南方日报：广东大学生球员 张健豪成“扣篮</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7454">珠江时报：依托创新平台构建国际合作新空间</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7432">人民日报海外版：三星助力创新 科技点亮梦</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7427">央广网：“岭南传统村落民俗文化与活化利用</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7426">南方日报：实施大德育工程 掀创新育人新浪</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7424">南方日报：实施大德育工程 掀创新育人新浪</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7418">南方网：广东哪家高校新媒体受师生欢迎？评</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7417">新快报：首届广东高校新媒体成果展示节在广</A></DIV></LI>
<LI>
<DIV><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1031&wbnewsid=7407">广州日报：广东启动建设首批省实验室  李希</A></DIV></LI>
</UL><script>_showDynClickBatch(['dynclicks_u9_7501','dynclicks_u9_7466','dynclicks_u9_7454','dynclicks_u9_7432','dynclicks_u9_7427','dynclicks_u9_7426','dynclicks_u9_7424','dynclicks_u9_7418','dynclicks_u9_7417','dynclicks_u9_7407'],[7501,7466,7454,7432,7427,7426,7424,7418,7417,7407],"wbnews", 1164291239)</script>
</DIV></DIV><!--媒体工大--><!--视频新闻-->
<DIV class="listrightc">
<DIV class="listrightcon">
<DIV class="listrightdh"><SPAN class="floatright"><A href="copy_1_meitigongdayinshipin.jsp?urltype=tree.TreeTempUrl&wbtreeid=1032"><IMG src="dfiles/20140/images/gdimg2.jpg"></A></SPAN><SPAN id="ctl00_ContentPlaceHolder1_ListRight1_lblspxw">视频新闻</SPAN></DIV>
<DIV class="videos"><script language="javascript" src="/system/resource/js/jquery/jquery-latest.min.js"></script>  <UL>
<LI><A class="spsmallimg" href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1032&wbnewsid=5401"><IMG src="/__local/E/6B/30/33842AAE2B9FCC23EFCBCFF1EA7_4F05EDCD_22EE.jpg" width="132" height="88"></A> 
<DIV style="width:132px; height:20px;line-height:20px;overflow:hidden;"><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1032&wbnewsid=5401">广东工业大学宣传片</A></DIV><SPAN class="floatright"><IMG src="dfiles/20140/images/spico02.jpg"><span id="dynclicks_u10_5401" name="dynclicks_u10_5401"></span></SPAN><FONT size="+0">2016-06-02</FONT> </LI>
<LI><A class="spsmallimg" href="http://www.iqiyi.com/w_19rw75otm9.html"><IMG src="/__local/0/B1/45/E65F6A5080A855EFB4CC1E7D913_72F8018D_54A88.png" width="132" height="88"></A> 
<DIV style="width:132px; height:20px;line-height:20px;overflow:hidden;"><A href="http://www.iqiyi.com/w_19rw75otm9.html">爱奇艺：张健豪——登上CB</A></DIV><SPAN class="floatright"><IMG src="dfiles/20140/images/spico02.jpg"><span id="dynclicks_u10_7468" name="dynclicks_u10_7468"></span></SPAN><FONT size="+0">2018-01-19</FONT> </LI>
</UL>
  <UL>
<LI><A class="spsmallimg" href="http://v.gdtv.cn/star/gdxwlb/2017-12-22/1216672.html"><IMG src="/__local/3/C4/78/A31C5FBA6DE16887692EAA09A23_A285BC49_745ED.png" width="132" height="88"></A> 
<DIV style="width:132px; height:20px;line-height:20px;overflow:hidden;"><A href="http://v.gdtv.cn/star/gdxwlb/2017-12-22/1216672.html">广东卫视：广东启动建设首</A></DIV><SPAN class="floatright"><IMG src="dfiles/20140/images/spico02.jpg"><span id="dynclicks_u10_7408" name="dynclicks_u10_7408"></span></SPAN><FONT size="+0">2017-12-25</FONT> </LI>
<LI><A class="spsmallimg" href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1032&wbnewsid=7374"><IMG src="/__local/0/B2/A2/25BD35ED64BFABCFFAFE5968552_F1961206_A5431.png" width="132" height="88"></A> 
<DIV style="width:132px; height:20px;line-height:20px;overflow:hidden;"><A href="meitizhongdaneirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1032&wbnewsid=7374">广东电视台：2017第二届PC</A></DIV><SPAN class="floatright"><IMG src="dfiles/20140/images/spico02.jpg"><span id="dynclicks_u10_7374" name="dynclicks_u10_7374"></span></SPAN><FONT size="+0">2017-12-19</FONT> </LI>
</UL>
<script>_showDynClickBatch(['dynclicks_u10_5401','dynclicks_u10_7468','dynclicks_u10_7408','dynclicks_u10_7374'],[5401,7468,7408,7374],"wbnews", 1164291239)</script>
</DIV>
<DIV class="clear"></DIV></DIV></DIV><!--视频新闻--></SPAN></DIV>
<DIV class="listleft">
<DIV class="listdaohang"><b>您现在的位置:</b>
               <a href="index.htm">网站首页</a>
                &gt;&gt;
              <a href="liebiaotupian.jsp?urltype=tree.TreeTempUrl&wbtreeid=1045">新闻头条</a>
</DIV>
<DIV class="contentmain">
<H3 class="yinti"><SPAN id="ctl00_ContentPlaceHolder1_tbxTitleIntact"></SPAN></H3>
<script language="javascript" src="_dwr/interface/NewsvoteDWR.js"></script><script language="javascript" src="_dwr/engine.js"></script><script language="javascript" src="/system/resource/js/news/newscontent.js"></script><script type="text/javascript">NewsvoteDWR.getNewsLinkUrl(7471,'1164291239','vsb',newsSkip);function newsSkip(data){if(data != ""){window.location.href = data;}}</script><LINK href="/system/resource/js/photoswipe/3.0.5.1/photoswipe.css" type=text/css rel=stylesheet><script language="javascript" src="/system/resource/js/photoswipe/3.0.5.1/klass.min.js"></script><LINK href="/system/resource/style/component/news/content/format2.css" type=text/css rel=stylesheet><script language="javascript" src="/system/resource/js/ajax.js"></script><form name="_newscontent_fromname">
<h1 class="title"><span id="ctl00_ContentPlaceHolder1_tbxTitle">学校2017年工作总结交流大会召开</span>
</h1>
<h3 class="fubiaoti"><span id="ctl00_ContentPlaceHolder1_tbxSubheading"></span>
 </h3>

<div class="info"><span class="floatright">字体：<a href="javascript:doZoom(9)">小</a> <a href="javascript:doZoom(10.5)" style="font-size:13px">
    中</a> <a href="javascript:doZoom(13)" style="font-size:14px">大</a></span>
<span id="ctl00_ContentPlaceHolder1_tbxUpdateTime">2018年01月23日</span> 
    浏览量：<span id="ctl00_ContentPlaceHolder1_lblHits"><script>_showDynClicks("wbnews", 1164291239, 7471)</script></span>次 


<span id="ctl00_ContentPlaceHolder1_tbxAuthor"> 作者：詹勇</span>  
<span id="ctl00_ContentPlaceHolder1_tbxEditor">摄影：韩君峰</span>
<span id="ctl00_ContentPlaceHolder1_tbxEditor"> 编辑：詹勇</span>
</div>
 <div id="ctl00_ContentPlaceHolder1_jj" class="jianjie"><p><span id="ctl00_ContentPlaceHolder1_tbxIntro">
    1月18日，学校在大学城校园召开2017年工作总结交流大会。校党委书记、校长陈新出席并讲话，强调要深入学习贯彻落实党的十九大精神，以习近平新时代中国特色社会主义思想为指引，扎实推进高水平大学建设。校党委副书记、纪委书记汤耀平主持。
    </span></p></div>  
<div class="content" id="contentText">
<div id='vsb_content_2' ><p class="vsbcontent_start"><strong><span style="font-size: 16px;">本网讯</span></strong><span style="font-size: 16px;"> 1月18日，学校在大学城校园召开2017年工作总结交流大会。校党委书记、校长陈新出席并讲话，强调要深入学习贯彻落实党的十九大精神，以习近平新时代中国特色社会主义思想为指引，扎实推进高水平大学建设。校党委副书记、纪委书记汤耀平主持。校党委副书记陈良友，副校长章云、陈立中、张光宇、王成勇、陈卓武、陈为民，副校级干部张学理出席会议。</span></p>
<p style="text-align: center;">
 <img width="600" src="/__local/7/C7/EB/D1EA65AE98167826A96039D9877_4C243B76_1AB2C.jpg" vwidth="600" vheight="" vurl="/_vsl/7C7EBD1EA65AE98167826A96039D9877/4C243B76/1AB2C" vsbhref="vurl" orisrc="/__local/7/C7/EB/D1EA65AE98167826A96039D9877_4C243B76_1AB2C.jpg" class="img_vsb_content"></p>
<p style="text-align: center;">
 <img width="600" src="/__local/3/BB/A9/4FEA7C3C92DB90F3B6C92D1B2A1_C6BEA315_3E75.jpg" vwidth="600" vheight="" vurl="/_vsl/3BBA94FEA7C3C92DB90F3B6C92D1B2A1/C6BEA315/3E75" vsbhref="vurl" orisrc="/__local/3/BB/A9/4FEA7C3C92DB90F3B6C92D1B2A1_C6BEA315_3E75.jpg" class="img_vsb_content"></p>
<p class="vsbcontent_start"><span style="font-size: 16px;">会上，发展规划处、学科办，研究生院、科技处、人事处、网络中心分别就高水平大学建设工作及学科建设情况、研究生人才培养工作、科技工作、人才队伍建设工作、信息化建设工作作了汇报，总结了2017年工作亮点与成效，提出了2018年工作设想。汤耀平宣读优秀研究生导师、先进科技工作者、科技工作先进集体、师德标兵、学科建设绩效奖、优秀教师、优秀教育工作者的表彰决定。校领导为受表彰个人、集体代表领奖。</span></p>
<p class="vsbcontent_start" style="text-align: center;">
 <img width="600" src="/__local/E/23/B4/786752B10740190BCA0745E25F7_452029EB_13B75.jpg" vwidth="600" vheight="" vurl="/_vsl/E23B4786752B10740190BCA0745E25F7/452029EB/13B75" vsbhref="vurl" orisrc="/__local/E/23/B4/786752B10740190BCA0745E25F7_452029EB_13B75.jpg" class="img_vsb_content"></p>
<p class="vsbcontent_start"><span style="font-size: 16px;">陈新讲话，首先对受表彰的个人和集体表示祝贺。他说，我们走过了不平凡的2017年，取得了不平凡的成绩，这归功于全校一大批有责任担当、不辱使命的领导干部、一线教师。但和时代的发展、国家的要求和省委省政府的重托相比，还有较大的差距。当前，全校正在深入学习贯彻落实党的十九大精神，要“大学习、深调研、真落实”，把习近平新时代中国特色社会主义思想融入血脉，进入灵魂，要以习近平总书记对广东的重要批示为目标，走在前列。新时代有新的使命，有新的责任和新的担当。当前，广东要建立国家科技产业创新中心，对标世界一流湾区来建设粤港澳大湾区，时代对我们的要求越来越高。前进路上会有各种艰难险阻，必须拿出巨大的勇气，凝聚磅礴的力量，要有国际眼光，去攻克一切困难，来迎接未来的挑战。</span></p>
<p><span style="font-size: 16px;">陈新指出，2018年是贯彻党的十九大精神的第一年、落实“十三五”规划的重要一年、推进高水平大学建设的关键一年。实践证明，只要“咬定青山不放松”，敢于挑战自己，在艰难中前行，就会赢得自己的掌声，赢得自己的感动。要重新审视自己，放眼世界，找准位置，继续向更高的目标迈进。接下来在新的一年，一要继续坚持从严治党，使党员干部的精气神更加显现，要推进从严治党向基层延伸，带领广大教师、一线工作人员有更好的精神面貌，去迎接新的挑战。二要加强学科规划，再出发。要加强学科交叉融合，促进学科平衡充分发展。要有更大的勇气、宏伟的目标，实现更大的挑战。三要加强科研能力建设，调动全校的积极性，实现重大科技成果有所突破。四要加强人才培养，坚持立德树人，培养能担当民族复兴大业的时代新人。每位教师要增强责任担当，言传身教，努力培养青年一代成为建设社会主义现代化强国的中坚力量。五要加强师资队伍建设。要激活存量，扩大增量。六要加强后勤改革和管理服务。要拿出铁的手腕，刮骨疗伤，正风肃纪。他强调要求，学习党的十九大精神重在“学懂、弄通、做实”，要有良好的精神状态，增强责任担当，以前所未有的速度向前发展，追求更高的发展质量。</span></p>
<p style="text-align: center;">
 <img width="600" src="/__local/C/04/05/9CB3EF01AF7DC638EB294B21232_A0CA7C6B_15E96.jpg" vwidth="600" vheight="" vurl="/_vsl/C04059CB3EF01AF7DC638EB294B21232/A0CA7C6B/15E96" vsbhref="vurl" orisrc="/__local/C/04/05/9CB3EF01AF7DC638EB294B21232_A0CA7C6B_15E96.jpg" class="img_vsb_content"></p>
<p><span style="font-size: 16px;">汤耀平在主持时强调要求，各部门各单位要认真学习、深刻领会、贯彻落实陈新书记、校长的讲话精神，准确把握新时代新方位新要求，推进高水平大学建设开新局立新功。</span></p>
<p><span style="font-size: 16px;"></span><span style="font-size: 16px;"></span><span style="font-size: 16px;"></span><span style="font-size: 16px;"></span><span style="font-size: 16px;"></span><span style="font-size: 16px;"><br></span></p>
<p style="text-align: center;">
 <img width="600" src="/__local/7/4B/8B/66B395DA957C8CCB3EBA29C14F6_F56530D9_16602.jpg" vwidth="600" vheight="" vurl="/_vsl/74B8B66B395DA957C8CCB3EBA29C14F6/F56530D9/16602" vsbhref="vurl" orisrc="/__local/7/4B/8B/66B395DA957C8CCB3EBA29C14F6_F56530D9_16602.jpg" class="img_vsb_content"></p>
<p style="text-align: center;"><span style="font-size: 16px;">校党委书记、校长陈新颁发学科建设绩效奖</span></p>
<p style="text-align: center;">
 <img width="600" src="/__local/F/62/13/514A197DACBEEB54AF37147EE8B_ABE3DF49_15C1C.jpg" vwidth="600" vheight="" vurl="/_vsl/F6213514A197DACBEEB54AF37147EE8B/ABE3DF49/15C1C" vsbhref="vurl" orisrc="/__local/F/62/13/514A197DACBEEB54AF37147EE8B_ABE3DF49_15C1C.jpg" class="img_vsb_content"></p>
<p style="text-align: center;"><span style="font-size: 16px;">校党委书记、校长陈新为优秀教师代表、优秀教育工作者代表颁奖</span></p>
<p style="text-align: center;">
 <img width="600" src="/__local/7/58/48/24BCC672242344A5946E03F7F57_BDAE672B_16A9F.jpg" vwidth="600" vheight="" vurl="/_vsl/7584824BCC672242344A5946E03F7F57/BDAE672B/16A9F" vsbhref="vurl" orisrc="/__local/7/58/48/24BCC672242344A5946E03F7F57_BDAE672B_16A9F.jpg" class="img_vsb_content"></p>
<p style="text-align: center;"><span style="font-size: 16px;">校党委副书记、纪委书记汤耀平，校党委副书记陈良友为师德标兵颁奖</span></p>
<p style="text-align: center;">
 <img width="600" src="/__local/E/08/72/CAA7E3A33B3E089E35075E5F13D_3F8CA7BD_16AA6.jpg" vwidth="600" vheight="" vurl="/_vsl/E0872CAA7E3A33B3E089E35075E5F13D/3F8CA7BD/16AA6" vsbhref="vurl" orisrc="/__local/E/08/72/CAA7E3A33B3E089E35075E5F13D_3F8CA7BD_16AA6.jpg" class="img_vsb_content"></p>
<p style="text-align: center;"><span style="font-size: 16px;">副校长章云、陈立中、张光宇为科技工作先进集体颁奖</span></p>
<p style="text-align: center;">
 <img width="600" src="/__local/4/2C/8C/2998851BBC31272BAE1A1A0261E_E3C6275A_172B4.jpg" vwidth="600" vheight="" vurl="/_vsl/42C8C2998851BBC31272BAE1A1A0261E/E3C6275A/172B4" vsbhref="vurl" orisrc="/__local/4/2C/8C/2998851BBC31272BAE1A1A0261E_E3C6275A_172B4.jpg" class="img_vsb_content"></p>
<p style="text-align: center;"><span style="font-size: 16px;">副校长王成勇、陈卓武为先进科技工作者代表颁奖</span></p>
<p style="text-align: center;">
 <img width="600" src="/__local/9/74/96/BC284D5AD9176C1F6D9409CFF09_960B8BB6_16C84.jpg" vwidth="600" vheight="" vurl="/_vsl/97496BC284D5AD9176C1F6D9409CFF09/960B8BB6/16C84" vsbhref="vurl" orisrc="/__local/9/74/96/BC284D5AD9176C1F6D9409CFF09_960B8BB6_16C84.jpg" class="img_vsb_content"></p>
<p style="text-align: center;"><span style="font-size: 16px;">副校长陈为民、副校级干部张学理为优秀研究生导师代表颁奖</span></p></div></div><div id="div_vote_id"></div>
    <input type="hidden" id="hid_link" value="" />
<div class="erweima">    
    <p><img src="dfiles/20140/images/39a7a9140edc951b3844ee109e1d1602.jpg" /><span>扫一扫<br />关注广东工业大学官方微信</span></p>
    <p><img src="dfiles/20140/images/fe61ea1f97abb61a65b3ecf9c8c8b84b.jpg" /><span>扫一扫<br />关注广东工业大学官方微博</span></p>
    <p><img src="dfiles/20140/images/bab566cfc98c18fed3687b2c0247f49e.jpg" /><span>扫一扫<br />手机看广东工业大学新闻网</span></p>
</div>
<div class="fenxianga">
<span class="floatright">
<div class="jiathis_style_24x24">
    <a class="jiathis_button_qzone"></a>
    <a class="jiathis_button_tsina"></a>
    <a class="jiathis_button_tqq"></a>
    <a class="jiathis_button_weixin"></a>
    <a class="jiathis_button_renren"></a>
    <a href="http://www.jiathis.com/share" class="jiathis jiathis_txt jtico jtico_jiathis" target="_blank"></a>
</div>
<script type="text/javascript" src="http://v3.jiathis.com/code/jia.js" charset="utf-8"></script>
</span><a href="#slj">[评论文章]</a>  <a href="#">
   <a href="javascript:window.close()">[关闭]</a>  <a href="javascript:history.go(-1);">
    [返回]</a></div> 
<div class="frontart">
   <br />
    下一篇：<span id="ctl00_ContentPlaceHolder1_lblsyp"><a href="neirongye.jsp?urltype=news.NewsContentUrl&wbtreeid=1045&wbnewsid=7323" >校党委理论学习中心组专题学习省委十二届二次全会精神</a></span>    
</div>  
    <p align=right>【<a href="javascript:window.opener=null;window.open('','_self');window.close();">关闭</a>】</p>
</form>

<DIV id="slj" class="artmes"><B>我来说两句</B> 
<DIV class="mesline">
<DIV class="line"></DIV></DIV></DIV></DIV></DIV>
<DIV class="clear"></DIV></DIV>
<DIV class="bottom">
<DIV class="bottomline">
<DIV class="bottomlinec"></DIV></DIV>
<DIV class="yqlj"><script type="text/javascript">
function linkall()
{
var h=document.getElementById('links').style.height;
if( h=="60px" )
{
document.getElementById('links').style.height="auto";
}
}
</script>
<DIV class="yqljtitle"><SPAN class="floatright"><IMG src="dfiles/20140/images/xsqb.jpg" onclick="linkall()"></SPAN>&nbsp;友情链接</DIV>
<DIV class="yqljcon">
<DIV id="links" style="height: 60px;overflow: hidden"><div class="yqljcon2">
<ul>
<li><A href="http://www.moe.gov.cn/" target="_blank">教育部</A></li>
<li><A href="http://www.xinhuanet.com/" target="_blank">新华网</A></li>
<li><A href="http://www.people.com.cn/" target="_blank">人民网</A></li>
<li><A href="http://www.gmw.cn/" target="_blank">光明网</A></li>
<li><A href="http://www.chinanews.com/index.shtml" target="_blank">中国新闻网</A></li>
<li><A href="http://www.chinaedu.edu.cn/" target="_blank">中国教育信息网</A></li>
<li><A href="http://digitalpaper.stdaily.com/" target="_blank">科技日报</A></li>
<li><A href="http://www.cyol.net/" target="_blank">中青在线</A></li>
<li><A href="http://www.southcn.com/" target="_blank">南方网</A></li>
<li><A href="http://www.ifeng.com/" target="_blank">凤凰网</A></li>
<li><A href="http://epaper.nfdaily.cn" target="_blank">南方日报</A></li>
<li><A href="http://www.ycwb.com/ePaper/ycwb/" target="_blank">羊城晚报</A></li>
<li><A href="http://gzdaily.dayoo.com" target="_blank">广州日报</A></li>
<li><A href="http://epaper.nandu.com/" target="_blank">南方都市报</A></li>
<li><A href="http://informationtimes.dayoo.com/" target="_blank">信息时报</A></li>
<li><A href="http://epaper.xkb.com.cn/" target="_blank">新快报</A></li>
<li><A href="http://epaper.gdkjb.com/" target="_blank">广东科技报</A></li>
</ul>
<div class="clear:both;"></div>
</div>

</DIV></DIV>
<DIV class="bottomcon"><!-- 版权内容请在本组件"内容配置-版权"处填写 -->
<P>Copyright@2013 gdutnews.gdut.edu.cn All Rights Reserved 广东工业大学党委宣传部 版权所有 </P>
<P>技术支持 网络信息与现代教育技术中心 电子邮箱：<A href="mailto:xwzx@gdut.edu.cn">xwzx@gdut.edu.cn</A> </P>
<P>建议使用IE7内核以上浏览器 </P></DIV></DIV></FORM></DIV>
<DIV></DIV>
<DIV></DIV>

</BODY></HTML>
"""

# base_url = "http://gdutnews.gdut.edu.cn"


class MyHtmlParser(HTMLParser):
    def __init__(self):
        self.find_title = False
        self.get_title = False
        self.find_content = False

        self.sub_div = None
        self.tag = None
        self.l_tag = None
        self.p_style = None

        self.title = None
        self.publish_date = None
        self.content = []
        self.img = []

        self.base_url = 'http://www.gdpu.edu.cn'

        super(MyHtmlParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        self.l_tag = self.tag
        self.tag = tag
        if tag == "div":
            for (variable, value) in attrs:
                if variable == 'class' and value == 'title text-center':
                    self.find_title = True

                if variable == 'class' and value == 'content':
                    self.find_content = True
                elif self.find_content and 'style' in variable:
                    self.sub_div = True
        elif tag == "h3" and self.find_title:
            self.get_title = True
        elif tag == "p" and self.find_content:
            for (variable, value) in attrs:
                if variable == "style" and value == "text-align: center;":
                    self.p_style = "center"
        elif tag == "span" and self.find_content:
            pass
        elif tag == 'img' and self.find_content:
            for (variable, value) in attrs:
                if variable == 'src':
                    image = "<image src='{}'></image>".format(urljoin(self.base_url, value))
                    self.content.append(image)

    def handle_endtag(self, tag):
        if tag == "div":
            if self.find_title:
                self.get_title = False
                self.find_title = False
            elif self.find_content and not self.sub_div:
                self.find_content = False
            elif self.sub_div:
                self.sub_div = False
        elif tag == "p":
            self.p_style = None
        self.tag = None

    def handle_data(self, data):
        data = data.strip()
        if not data:
            pass
        elif self.get_title and self.tag == "h3":
            self.title = data
        elif self.find_title and self.tag == "small":
            meta = re.match(".*发布时间：(.*?)\s来源：(.*?)\s", data)
            if meta:
                date_str = meta.group(1)
                self.publish_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        elif self.find_content:
            if self.tag == "span":
                if self.l_tag == "p":
                    if self.p_style == "center":
                        self.content.append(('<view class="center"><text>{}</text></view>'.format(data)))
                    else:
                        self.content.append(('<view ><text>{}</text></view>'.format(data)))
                elif self.l_tag == "strong":
                    pass
                else:
                    self.content.append("<view ><text>{}</text></view>".format(data))
            elif self.tag == "div" and self.l_tag == "span":
                self.content.append("<view ><text>{}</text></view>".format(data))


def parser(html):
    hp = MyHtmlParser()
    html = re.sub('<br />', '', html)
    hp.feed(html)
    hp.close()
    return hp


if __name__ == '__main__':
    hp = parser(html1)
    print(hp.publish_date)