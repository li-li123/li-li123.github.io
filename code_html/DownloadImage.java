package test;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * @author WangNing yogehaoren@gamil.com <br>
 * @since 1.0
 */
public class DownloadImage {

    /**
     * 替换后的 图片前缀
     */
    private static final String URL_PRE = "https://ning-wang.oss-cn-beijing.aliyuncs.com/blog-imags/";

    /**
     *
     * 图片 正则表达式
     */
    private static final String IMAGE_PATTERN = ".*(https://static001.geekbang.org.*.(jpg|jpeg|png)).*";

    /**
     * sidebar 目录前缀
     */
    private static final String SIDEBAR_PRE = "god/jk_redis";


    public static void main(String[] args) {
        OkHttpClient client = new OkHttpClient();

        // md 文件夹
        File rootFile = new File("C:\\Users\\PC\\Desktop\\jk_mysql");
        // 暂存图片文件
        String tempImageDir = "C:\\Users\\PC\\Desktop\\temp";

        if(!new File(tempImageDir).exists()){
            new File(tempImageDir).mkdirs();
        }

        Stack<File> mdStack = new Stack<>();
        mdStack.push(rootFile);
        ArrayList<File> files = new ArrayList<>();

        // 搜索 md 文件
        while (!mdStack.isEmpty()){

            File pop = mdStack.pop();
            if(pop!=null&&pop.exists()){

                if(pop.isFile()){
                    if(pop.getName().endsWith(".md")){

                        files.add(renameFile(pop));

                    }
                }else if(pop.isDirectory()){
                    File[] childFiles = pop.listFiles();

                    if(childFiles!=null && childFiles.length >0){

                        for(File element:childFiles){

                            if(element.isDirectory()){
                                mdStack.push(element);
                            }else if(element.isFile() && element.getName().endsWith(".md")){

                                files.add(renameFile(element));
                            }

                        }

                    }

                }

            }

        }


        // 搜索并替换 图片
        List<String> imageUrl = new ArrayList<>();

        for(File element:files){

            Pattern compile = Pattern.compile(IMAGE_PATTERN);
            try {
                List<String> newLines = new ArrayList<>();
                Stream<String> lines = Files.lines(Paths.get(element.getAbsolutePath()));
                lines.forEach(line->{
                        Matcher matcher = compile.matcher(line);
                        if (matcher.find()){
                            String oldUrl = matcher.group(1);
                            imageUrl.add(oldUrl);
                            newLines.add(getNewLine(oldUrl));
                            System.out.println(" find image : " + oldUrl);
                        }else{
                            newLines.add(line);
                        }

                });
                String collected = newLines.stream().collect(Collectors.joining("\n"));
                Files.write(element.toPath(), collected.getBytes(), StandardOpenOption.WRITE , StandardOpenOption.CREATE);


            } catch (Throwable e) {
                e.printStackTrace();
            }
        }

        // 下载图片
        downloadImage(imageUrl, client, tempImageDir);

        // 生成目录
        createSidebar(files, rootFile.getAbsolutePath());

        System.out.println("Over!");


    }

    /**
     * 替换 图片
     * @param oldUrl
     * @return -
     */
    private static String getNewLine(String oldUrl){

        String start = "<center><img src=\"";

        String end = "\" style=\"zoom:50%;\" /></center>";


        String[] split = oldUrl.split("/");
        String newUrl = URL_PRE + split[split.length-1];

        return start + newUrl + end;

    }

    /**
     * 下载图片
     * @param images
     * @param client
     * @param rootDir
     */
    private static void downloadImage(List<String> images, OkHttpClient client, String rootDir){
        for(String url :images){

            Request request = new Request.Builder().url(url).build();

            try(Response response = client.newCall(request).execute()){
                System.out.println("Success Download file : "+url);
                String[] split = url.split("/");

                InputStream inputStream = response.body().byteStream();

                Files.copy(inputStream, Paths.get(rootDir, split[split.length-1]), StandardCopyOption.REPLACE_EXISTING);


            } catch (IOException e) {
                e.printStackTrace();
            }

        }
        System.out.println("生成目录成功");

    }

    /**
     * 重命名文本
     * @param file -
     * @return -
     */
    public static File renameFile(File file){
        String absolutePath = file.getAbsolutePath();
        absolutePath = absolutePath.replace(" ", "");
        absolutePath = absolutePath.replace("\"", "");
        absolutePath = absolutePath.replace("'", "");
        absolutePath = absolutePath.replace("“", "");
        absolutePath = absolutePath.replace("”", "");
        absolutePath = absolutePath.replace("_.md", ".md");
        absolutePath = absolutePath.replace("，", "_");
        absolutePath = absolutePath.replace("？", "");
        absolutePath = absolutePath.replace("（", "");
        absolutePath = absolutePath.replace("）", "");
        absolutePath = absolutePath.replace("：", "_");
        absolutePath = absolutePath.replace("~", "_");
        absolutePath = absolutePath.replace("、", "_");
        absolutePath = absolutePath.replace("～", "_");
        absolutePath = absolutePath.replace("__", "_");
        absolutePath = absolutePath.replace("___", "_");
        File newFile   = new File(absolutePath);
        file.renameTo(newFile);
        return newFile;

    }

    private static void createSidebar(List<File> files, String rootDir){

        File sidebarFile = new File(rootDir + "/_sidebar.md");

        StringBuilder sb = new StringBuilder();
        sb.append("> <center> 摘要 </center>").append("\n\n");
        for(File file:files){

            sb.append("* ").append("[").append(file.getName().replace(".md", "").replace("_", " ")).append("]")
                    .append("(").append(SIDEBAR_PRE).append("/").append(file.getName()).append(")\n");

        }

        try {
            if(sidebarFile.exists()){
                sidebarFile.delete();
            }
            Files.write(sidebarFile.toPath(), sb.toString().getBytes(),
                    StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE, StandardOpenOption.CREATE);
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

}
